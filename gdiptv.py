#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
广东 IPTV 自动更新脚本（优化 FOFA 查询和 IP 验证）
"""
import os
import requests
import base64
import json
import re
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import cv2

# ===================== 环境变量 ===================== #
FOFA_EMAIL = os.getenv("FOFA_EMAIL")
FOFA_KEY = os.getenv("FOFA_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")  # username/repo
IPTV_TXT_URL = os.getenv("IPTV_TXT_URL", "gdiptv.txt")
IPTV_M3U_URL = os.getenv("IPTV_M3U_URL", "gdiptv.m3u")
MAX_THREADS = int(os.getenv("MAX_THREADS", "10"))

# ===================== 分组与查询绑定 ===================== #
GROUP_QUERIES = {
    "广东频道[A]": 'server="udpxy" && region="Guangdong" && org="Chinanet"',
    "广东频道[B]": 'server="udpxy" && city="Shenzhen" && org="Chinanet"',
    "广东频道[C]": 'server="udpxy" && city="Guangzhou" && org="Chinanet"',
    "广东频道[D]": 'server="udpxy" && city="Huizhou" && org="Chinanet"'
}

# ===================== FOFA 查询 ===================== #
def query_fofa(query):
    qbase64 = base64.b64encode(query.encode()).decode()
    api_url = f"https://fofa.info/api/v1/search/all?email={FOFA_EMAIL}&key={FOFA_KEY}&qbase64={qbase64}&size=100"
    try:
        r = requests.get(api_url, timeout=15)
        data = r.json()
        if data.get("error"):
            print(f"[FOFA] 错误: {data.get('errmsg', '未知错误')}")
            return []
        results = data.get("results", [])
        return [item[0].replace("http://", "").replace("https://", "").strip("/") for item in results]
    except Exception as e:
        print(f"[FOFA] 请求失败: {e}")
        return []

# ===================== IP 验证 ===================== #
def verify_udp(ip_port):
    """尝试打开测试流，验证 udpxy 是否可用"""
    test_url = f"http://{ip_port}/udp/239.77.0.1:5146"
    try:
        cap = cv2.VideoCapture(test_url)
        if cap.isOpened():
            cap.release()
            return True
    except:
        pass
    return False

def get_first_valid_ip(ips):
    """并发验证 IP，返回第一个可用的"""
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        future_to_ip = {executor.submit(verify_udp, ip): ip for ip in ips}
        for future in as_completed(future_to_ip):
            ip = future_to_ip[future]
            try:
                if future.result():
                    return ip
            except Exception:
                continue
    return None

# ===================== IPTV 文件操作 ===================== #
def download_file(url):
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return r.text

def update_txt_ips(content, group_name, new_ip_port, fail_ip="88.88.88.88:8888"):
    lines = content.splitlines()
    in_group = False
    new_lines = []

    for line in lines:
        if line.startswith(group_name):
            in_group = True
            if new_ip_port:
                line = re.sub(r"失效", "", line)
            else:
                if "失效" not in line:
                    line = line.replace("#genre#", "失效,#genre#")
            new_lines.append(line)
            continue

        if any(line.startswith(g) for g in GROUP_QUERIES.keys()) and line != group_name:
            in_group = False

        if in_group and line.strip() and "," in line:
            name, url = line.split(",", 1)
            if new_ip_port:
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

def update_m3u_ips(m3u_content, group_name, new_ip_port, fail_ip="88.88.88.88:8888"):
    lines = m3u_content.splitlines()
    in_group = False
    updated_lines = []
    url_pattern = re.compile(r"http://\d{1,3}(?:\.\d{1,3}){3}:\d+")

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#EXTINF") and f"group-title=\"{group_name}\"" in stripped:
            in_group = True
            updated_lines.append(line)
            continue

        if in_group and stripped.startswith("http://"):
            new_line = url_pattern.sub(f"http://{new_ip_port}" if new_ip_port else f"http://{fail_ip}", stripped)
            updated_lines.append(new_line)
            in_group = False
        else:
            updated_lines.append(line)
    return "\n".join(updated_lines)

# ===================== GitHub 上传 ===================== #
def push_to_github(file_path, content, commit_message):
    api_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{file_path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    get_resp = requests.get(api_url, headers=headers)
    sha = get_resp.json().get("sha", "")
    encoded = base64.b64encode(content.encode()).decode()
    payload = {"message": commit_message, "content": encoded}
    if sha:
        payload["sha"] = sha
    r = requests.put(api_url, headers=headers, data=json.dumps(payload))
    if r.status_code in [200, 201]:
        print(f"[GitHub] ✅ 文件已更新: {file_path}")
    else:
        print(f"[GitHub] ❌ 更新失败: {r.text}")

# ===================== 主流程 ===================== #
def main():
    txt = download_file(IPTV_TXT_URL)
    m3u = download_file(IPTV_M3U_URL)

    for group_name, query in GROUP_QUERIES.items():
        print(f"=== 处理分组 {group_name} ===")
        ips = query_fofa(query)
        ips = list(dict.fromkeys(ips))
        valid_ip = get_first_valid_ip(ips)
        if valid_ip:
            print(f"[{group_name}] 使用 IP: {valid_ip}")
        else:
            print(f"[{group_name}] ❌ 未找到可用 IP，将使用临时失效 IP")
            valid_ip = None

        txt = update_txt_ips(txt, group_name, valid_ip)
        m3u = update_m3u_ips(m3u, group_name, valid_ip)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    txt = re.sub(r"# 更新时间:.*", "", txt).strip() + f"\n# 更新时间: {now}"
    m3u = re.sub(r"# 更新时间:.*", "", m3u).strip() + f"\n# 更新时间: {now}"

    push_to_github("gdiptv.txt", txt, f"Update IPTV TXT {now}")
    push_to_github("gdiptv.m3u", m3u, f"Update IPTV M3U {now}")

if __name__ == "__main__":
    main()
