#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
广东 IPTV 自动更新脚本 (适用于 GitHub Actions)
作者: CCAV
说明:
 - 从 FOFA 自动查询广东地区 udpxy 源。
 - 验证可用后替换 IPTV 文件中对应组的 IP。
 - 如果组无可用 IP，group-title 添加“失效”；成功获取 IP 则删除“失效”。
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

# ============ FOFA 查询与分组绑定 ============ #
FOFA_GROUPS = [
    {"query": 'server="udpxy" && region="Guangdong" && org="Chinanet"', "group": "广东频道[A]"},
    {"query": 'server="udpxy" && city="Shenzhen" && org="Chinanet"', "group": "广东频道[B]"},
    {"query": 'server="udpxy" && city="Huizhou" && org="Chinanet"', "group": "广东频道[C]"},
    {"query": 'server="udpxy" && city="Guangzhou" && org="Chinanet"', "group": "广东频道[D]"}
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
        return [item[0].replace("http://", "").replace("https://", "").strip("/") for item in results]
    except Exception as e:
        print(f"[FOFA] 请求失败: {e}")
        return []

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

def download_file(url):
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return r.text

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

def update_group_ip_m3u(content, group_name, new_ip_port):
    """按组替换 m3u 中的 IP 并更新失效标记"""
    pattern_group = re.compile(rf"(?<=#GROUP:{re.escape(group_name)})(.*?)(?=(#GROUP:|$))", re.S)
    group_content = pattern_group.search(content)
    if not group_content:
        return content
    text = group_content.group(1)
    # 替换 IP 或添加失效
    if new_ip_port:
        text_new = re.sub(r"http://\d{1,3}(?:\.\d{1,3}){3}:\d+(?=/udp/)", f"http://{new_ip_port}", text)
        text_new = re.sub(r'group-title="([^"]*)失效"', r'group-title="\1"', text_new)
    else:
        def add_invalid(m):
            name = m.group(1)
            if "失效" not in name:
                return f'group-title="{name}失效"'
            return m.group(0)
        text_new = re.sub(r'group-title="([^"]*)"', add_invalid, text)
    return content[:group_content.start(1)] + text_new + content[group_content.end(1):]

def update_group_ip_txt(content, group_name, new_ip_port):
    """按组替换 txt 中的 IP 或标记失效"""
    pattern_group = re.compile(rf"(?<=#GROUP:{re.escape(group_name)})(.*?)(?=(#GROUP:|$))", re.S)
    group_content = pattern_group.search(content)
    if not group_content:
        return content
    text = group_content.group(1)
    lines = text.splitlines()
    lines_new = []
    for line in lines:
        if not line.strip():
            lines_new.append(line)
            continue
        if new_ip_port:
            line_new = re.sub(r"http://\d{1,3}(?:\.\d{1,3}){3}:\d+", f"http://{new_ip_port}", line)
            line_new = line_new.replace("失效", "")
            lines_new.append(line_new)
        else:
            if "失效" not in line:
                lines_new.append(line + " 失效")
            else:
                lines_new.append(line)
    text_new = "\n".join(lines_new)
    return content[:group_content.start(1)] + text_new + content[group_content.end(1):]

# ============ 主流程 ============ #
def main():
    txt = download_file(IPTV_TXT_URL)
    m3u = download_file(IPTV_M3U_URL)

    for group in FOFA_GROUPS:
        query = group["query"]
        group_name = group["group"]

        all_ips = query_fofa(query)
        valid_ip = None
        for ip_port in all_ips:
            if verify_udp(ip_port):
                valid_ip = ip_port
                break

        if valid_ip:
            print(f"[组 {group_name}] ✅ 使用 IP: {valid_ip}")
        else:
            print(f"[组 {group_name}] ❌ 没有可用 IP")

        m3u = update_group_ip_m3u(m3u, group_name, valid_ip)
        txt = update_group_ip_txt(txt, group_name, valid_ip)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    txt += f"\n# 更新时间: {now}"
    m3u += f"\n# 更新时间: {now}"

    push_to_github("gdiptv.txt", txt, f"Update IPTV TXT {now}")
    push_to_github("gdiptv.m3u", m3u, f"Update IPTV M3U {now}")

if __name__ == "__main__":
    main()
