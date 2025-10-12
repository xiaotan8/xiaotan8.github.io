#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
广东 IPTV 自动更新脚本 (适用于 GitHub Actions)
作者: CCAV
说明:
 - 从 FOFA 自动查询广东地区 udpxy 源。
 - 验证可用后替换 IPTV 文件中的每组 IP。
 - 失效线路统一替换为 88.88.88.88:888 并加失效标记。
 - 使用 FOFA、GitHub API 自动更新远程仓库。
"""
import os
import requests
import base64
import json
import re
from datetime import datetime
import cv2

# ============ 环境变量 ============ #
FOFA_EMAIL = os.getenv("FOFA_EMAIL")
FOFA_KEY = os.getenv("FOFA_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")  # 形如 "username/repo"
IPTV_TXT_URL = os.getenv("IPTV_TXT_URL", "gdiptv.txt")
IPTV_M3U_URL = os.getenv("IPTV_M3U_URL", "gdiptv.m3u")

# ============ FOFA 查询配置 ============ #
FOFA_QUERIES = {
    "广东频道[A]": 'server="udpxy" && region="Guangdong" && org="Chinanet"',
    "广东频道[B]": 'server="udpxy" && city="Shenzhen" && org="Chinanet"',
    "广东频道[C]": 'server="udpxy" && city="Huizhou" && org="Chinanet"',
    "广东频道[D]": 'server="udpxy" && city="Guangzhou" && org="Chinanet"'
}

TEMP_FAIL_IP = "88.88.88.88:888"  # 临时失效替换 IP

# ============ FOFA 查询 ============ #
def query_fofa(query):
    qbase64 = base64.b64encode(query.encode()).decode()
    api_url = f"https://fofa.info/api/v1/search/all?email={FOFA_EMAIL}&key={FOFA_KEY}&qbase64={qbase64}&size=1000"
    try:
        r = requests.get(api_url, timeout=15)
        data = r.json()
        if data.get("error"):
            print(f"[FOFA] 错误: {data.get('errmsg', '未知错误')}")
            return []
        results = data.get("results", [])
        print(f"[FOFA] 返回 {len(results)} 条结果")
        return [item[0].replace("http://", "").replace("https://", "").strip("/") for item in results]
    except Exception as e:
        print(f"[FOFA] 请求失败: {e}")
        return []

def verify_udp(ip_port):
    """尝试打开测试流，验证 udpxy 是否可用"""
    test_url = f"http://{ip_port}/udp/239.77.0.1:5146"
    try:
        cap = cv2.VideoCapture(test_url)
        if cap.isOpened():
            cap.release()
            print(f"[验证成功] {ip_port}")
            return True
    except Exception:
        pass
    print(f"[验证失败] {ip_port}")
    return False

# ============ IPTV 文件处理 ============ #
def download_file(url):
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return r.text

def update_group_ips(content, group_name, new_ip_port, fail_ip=TEMP_FAIL_IP):
    """
    替换该分组内所有频道 IP，更新失效标记
    如果 new_ip_port 为 None，则替换为 fail_ip 并加失效标记
    """
    lines = content.splitlines()
    in_group = False
    has_valid_ip = new_ip_port is not None
    new_lines = []

    for line in lines:
        # 分组标题
        if line.startswith(group_name):
            in_group = True
            if has_valid_ip:
                line = re.sub(r"失效", "", line)
            else:
                if "失效" not in line:
                    line = line.replace(group_name, f"{group_name}失效")
            new_lines.append(line)
            continue

        # 判断是否进入下一组
        if any(line.startswith(g) for g in FOFA_QUERIES.keys()) and line != group_name:
            in_group = False

        # 处理分组内频道行
        if in_group and line.strip() and "," in line:
            name, url = line.split(",", 1)
            if group_name in name:
                if has_valid_ip:
                    url = re.sub(r"http://\d{1,3}(?:\.\d{1,3}){3}:\d+", f"http://{new_ip_port}", url)
                    name = re.sub(r"失效", "", name)
                else:
                    url = re.sub(r"http://\d{1,3}(?:\.\d{1,3}){3}:\d+", f"http://{fail_ip}", url)
                    if "失效" not in name:
                        name = f"{name}失效"
            new_lines.append(f"{name},{url}")
        else:
            new_lines.append(line)
    return "\n".join(new_lines)

# ============ GitHub 上传 ============ #
def push_to_github(file_path, content, commit_message):
    api_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{file_path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    get_resp = requests.get(api_url, headers=headers)
    sha = get_resp.json().get("sha", "")
    encoded = base64.b64encode(content.encode()).decode()
    payload = {"message": commit_message, "content": encoded, "sha": sha}
    r = requests.put(api_url, headers=headers, data=json.dumps(payload))
    if r.status_code in [200, 201]:
        print(f"[GitHub] ✅ 文件已更新: {file_path}")
    else:
        print(f"[GitHub] ❌ 更新失败: {r.text}")

# ============ 主流程 ============ #
def main():
    txt = download_file(IPTV_TXT_URL)
    m3u = download_file(IPTV_M3U_URL)

    for group_name, query in FOFA_QUERIES.items():
        print(f"=== 处理分组 {group_name} ===")
        all_ips = query_fofa(query)
        all_ips = list(dict.fromkeys(all_ips))
        valid_ip = None
        for ip_port in all_ips:
            if verify_udp(ip_port):
                valid_ip = ip_port
                break
        if valid_ip:
            print(f"[{group_name}] 使用 IP: {valid_ip}")
        else:
            print(f"[{group_name}] ❌ 未找到可用 IP，将使用临时失效 IP {TEMP_FAIL_IP}")
        txt = update_group_ips(txt, group_name, valid_ip)
        m3u = update_group_ips(m3u, group_name, valid_ip)

    # 更新时间
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    txt = re.sub(r"# 更新时间:.*", "", txt).strip()
    m3u = re.sub(r"# 更新时间:.*", "", m3u).strip()
    txt += f"\n# 更新时间: {now}"
    m3u += f"\n# 更新时间: {now}"

    push_to_github("gdiptv.txt", txt, f"Update IPTV TXT {now}")
    push_to_github("gdiptv.m3u", m3u, f"Update IPTV M3U {now}")

if __name__ == "__main__":
    main()
