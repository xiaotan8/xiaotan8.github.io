#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
广东 IPTV 自动更新脚本 (适用于 GitHub Actions)
作者: CCAV
功能:
 - 从 FOFA 自动查询广东地区 udpxy 源，每组获取最优 IP。
 - 根据 IP 更新 IPTV TXT/M3U 文件，每组对应不同 IP。
 - 频道 group-title 增删“失效”标识。
 - 更新时间覆盖，不累积。
"""
import os
import requests
import base64
import json
import re
import cv2
from datetime import datetime

# ============ 环境变量 ============ #
FOFA_EMAIL = os.getenv("FOFA_EMAIL")
FOFA_KEY = os.getenv("FOFA_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")  # username/repo
IPTV_TXT_URL = os.getenv("IPTV_TXT_URL", "gdiptv.txt")
IPTV_M3U_URL = os.getenv("IPTV_M3U_URL", "gdiptv.m3u")

# ============ FOFA 查询和分组名称绑定 ============ #
FOFA_QUERIES = [
    'server="udpxy" && region="Guangdong" && org="Chinanet"',
    'server="udpxy" && city="Shenzhen" && org="Chinanet"',
    'server="udpxy" && city="Huizhou" && org="Chinanet"',
    'server="udpxy" && city="Guangzhou" && org="Chinanet"'
]
GROUP_NAMES = [
    "广东频道[A]",
    "广东频道[B]",
    "广东频道[C]",
    "广东频道[D]"
]

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

# ============ 验证 UDP IP ============ #
def verify_udp(ip_port):
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

def update_group_ip(content, group_name, ip_port):
    """
    替换该组 IP，并更新失效标记
    """
    # 判断是否需要添加/删除“失效”
    if ip_port:
        # 移除失效标记
        group_pattern = re.compile(rf'{re.escape(group_name)}失效?')
        content = group_pattern.sub(group_name, content)
    else:
        # 添加失效标记
        if "失效" not in group_name:
            group_name_with_fail = f"{group_name}失效"
        else:
            group_name_with_fail = group_name
        group_pattern = re.compile(rf'{re.escape(group_name)}(?!失效)')
        content = group_pattern.sub(group_name_with_fail, content)

    if ip_port:
        # 替换该组 IP
        # 找到该组所在段落，以 #GROUP:group_name 开头，直到下一个 #GROUP 或文件结束
        group_regex = re.compile(rf"(#GROUP:{re.escape(group_name)}.*?)(?=(#GROUP:)|$)", re.DOTALL)
        def repl(m):
            segment = m.group(1)
            pattern = re.compile(r"http://\d{1,3}(?:\.\d{1,3}){3}:\d+(?=/udp/)")
            return pattern.sub(f"http://{ip_port}", segment)
        content = group_regex.sub(repl, content)
    return content

def update_timestamp(content):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 替换原有更新时间
    timestamp_pattern = re.compile(r"# 更新时间:.*")
    if timestamp_pattern.search(content):
        content = timestamp_pattern.sub(f"# 更新时间: {now}", content)
    else:
        content += f"\n# 更新时间: {now}"
    return content

# ============ GitHub 上传 ============ #
def push_to_github(file_path, content, commit_message):
    api_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{file_path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    get_resp = requests.get(api_url, headers=headers)
    sha = get_resp.json().get("sha", "")
    encoded = base64.b64encode(content.encode()).decode()
    payload = {
        "message": commit_message,
        "content": encoded,
        "sha": sha
    }
    r = requests.put(api_url, headers=headers, data=json.dumps(payload))
    if r.status_code in [200, 201]:
        print(f"[GitHub] ✅ 文件已更新: {file_path}")
    else:
        print(f"[GitHub] ❌ 更新失败: {r.text}")

# ============ 主流程 ============ #
def main():
    txt = download_file(IPTV_TXT_URL)
    m3u = download_file(IPTV_M3U_URL)

    for group_name, query in zip(GROUP_NAMES, FOFA_QUERIES):
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
            print(f"[{group_name}] ❌ 没有可用 IP")

        txt = update_group_ip(txt, group_name, valid_ip)
        m3u = update_group_ip(m3u, group_name, valid_ip)

    txt = update_timestamp(txt)
    m3u = update_timestamp(m3u)

    push_to_github("gdiptv.txt", txt, f"Update IPTV TXT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    push_to_github("gdiptv.m3u", m3u, f"Update IPTV M3U {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
