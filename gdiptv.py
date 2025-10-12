#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
广东 IPTV 自动更新脚本 (适用于 GitHub Actions)
作者: CCAV
说明:
 - 从 FOFA 自动查询广东地区 udpxy 源。
 - 验证可用后替换 IPTV 文件中的全部 http://IP:PORT。
 - 使用 FOFA、GitHub API 自动更新远程仓库。
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
GITHUB_REPO = os.getenv("GITHUB_REPO")  # 形如 "username/repo"
IPTV_TXT_URL = os.getenv("IPTV_TXT_URL", "gdiptv.txt")
IPTV_M3U_URL = os.getenv("IPTV_M3U_URL", "gdiptv.m3u")

# ============ FOFA 查询配置 ============ #
FOFA_QUERIES = [
    'server="udpxy" && region="Guangdong" && org="Chinanet"',
    'server="udpxy" && city="Shenzhen" && org="Chinanet"',
    'server="udpxy" && city="Huizhou" && org="Chinanet"',
    'server="udpxy" && city"Guangzhou" && org="Chinanet"'
]

# ============ 辅助函数 ============ #
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
        # 返回 host:port 格式
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

def update_ip_in_file(content, new_ip_port):
    """
    替换所有 http://IP:PORT/udp/... 为 http://new_ip_port/udp/...
    始终使用完整 ip:port 模式（不保留旧端口）
    """
    pattern = re.compile(r"http://\d{1,3}(?:\.\d{1,3}){3}:\d+(?=/udp/)")
    return pattern.sub(f"http://{new_ip_port}", content)

def download_file(url):
    """下载远程文件"""
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return r.text

def push_to_github(file_path, content, commit_message):
    """上传文件到 GitHub"""
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
    all_ips = []
    for q in FOFA_QUERIES:
        all_ips.extend(query_fofa(q))
    all_ips = list(dict.fromkeys(all_ips))  # 去重

    valid_ip = None
    for ip_port in all_ips:
        if verify_udp(ip_port):
            valid_ip = ip_port
            break

    if not valid_ip:
        print("❌ 没有找到可用的 udpxy 地址")
        return

    print(f"✅ 使用 IP: {valid_ip}")

    txt = download_file(IPTV_TXT_URL)
    m3u = download_file(IPTV_M3U_URL)

    txt_new = update_ip_in_file(txt, valid_ip)
    m3u_new = update_ip_in_file(m3u, valid_ip)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    txt_new += f"\n# 更新时间: {now}"
    m3u_new += f"\n# 更新时间: {now}"

    push_to_github("gdiptv.txt", txt_new, f"Update IPTV TXT {now}")
    push_to_github("gdiptv.m3u", m3u_new, f"Update IPTV M3U {now}")

if __name__ == "__main__":
    main()
