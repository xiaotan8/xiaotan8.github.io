#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
广东 IPTV 自动更新脚本（优化版）
支持：FOFA查询、CV2验证、TXT+M3U同步更新、失效标记、GitHub推送
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
GITHUB_REPO = os.getenv("GITHUB_REPO")  # 例: "ccavxxx/IPTV"
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

FAIL_IP = "88.88.88.88:888"

# ===================== FOFA 查询 ===================== #
def query_fofa(query):
    qbase64 = base64.b64encode(query.encode()).decode()
    api_url = f"https://fofa.info/api/v1/search/all?email={FOFA_EMAIL}&key={FOFA_KEY}&qbase64={qbase64}&size=100&fields=host"
    try:
        r = requests.get(api_url, timeout=15)
        data = r.json()
        if data.get("error"):
            print(f"[FOFA] 错误: {data.get('errmsg', '未知错误')}")
            return []
        results = data.get("results", [])
        return [host.replace("http://", "").replace("https://", "").strip("/") for host in results]
    except Exception as e:
        print(f"[FOFA] 请求失败: {e}")
        return []

# ===================== IP 验证 ===================== #
def verify_udp(ip_port):
    """尝试用 OpenCV 打开 UDP 流"""
    test_url = f"http://{ip_port}/udp/239.77.0.1:5146"
    try:
        cap = cv2.VideoCapture(test_url)
        if cap.isOpened():
            cap.release()
            return True
    except Exception:
        pass
    return False


def get_first_valid_ip(ips):
    """并发验证IP，返回第一个可用IP"""
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = {executor.submit(verify_udp, ip): ip for ip in ips}
        for future in as_completed(futures):
            ip = futures[future]
            try:
                if future.result():
                    return ip
            except Exception:
                continue
    return None

# ===================== IPTV 文件更新 ===================== #
def update_txt_ips(content, group_name, new_ip_port):
    lines = content.splitlines()
    in_group = False
    result = []
    for line in lines:
        if line.startswith(group_name):
            in_group = True
            # 处理失效标记
            if new_ip_port:
                line = re.sub(r"失效", "", line)
            else:
                if "失效" not in line:
                    line = line.replace("#genre#", "失效#genre#")
            result.append(line)
            continue

        # 离开分组
        if any(line.startswith(g) for g in GROUP_QUERIES.keys()) and not line.startswith(group_name):
            in_group = False

        if in_group and "," in line:
            name, url = line.split(",", 1)
            url = re.sub(r"http://[\d\.]+:\d+", f"http://{new_ip_port or FAIL_IP}", url)
            if new_ip_port:
                name = name.replace("失效", "")
            else:
                if "失效" not in name:
                    name = f"{name}失效"
            result.append(f"{name},{url}")
        else:
            result.append(line)
    return "\n".join(result)


def update_m3u_ips(content, group_name, new_ip_port):
    """更新 M3U 文件 IP + group-title 失效状态"""
    lines = content.splitlines()
    updated = []
    in_group = False
    url_pattern = re.compile(r"http://[\d\.]+:\d+")
    group_pattern = re.compile(rf'group-title="{group_name}(?:\[失效\])?"')

    for line in lines:
        # 检测组头
        if "#EXTINF" in line and f'group-title="' in line:
            if group_name in line:
                in_group = True
                if new_ip_port:
                    # 删除失效标记
                    line = re.sub(rf'{re.escape(group_name)}\[失效\]', group_name, line)
                else:
                    # 添加失效标记
                    if f"{group_name}[失效]" not in line:
                        line = line.replace(group_name, f"{group_name}[失效]")
            else:
                in_group = False
            updated.append(line)
            continue

        # 替换URL
        if in_group and line.strip().startswith("http://"):
            new_line = url_pattern.sub(f"http://{new_ip_port or FAIL_IP}", line)
            updated.append(new_line)
            in_group = False
        else:
            updated.append(line)
    return "\n".join(updated)


# ===================== GitHub 上传 ===================== #
def push_to_github(file_path, content, message):
    api_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{file_path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    encoded = base64.b64encode(content.encode()).decode()

    sha = ""
    resp = requests.get(api_url, headers=headers)
    if resp.status_code == 200:
        sha = resp.json().get("sha", "")

    payload = {"message": message, "content": encoded}
    if sha:
        payload["sha"] = sha

    put = requests.put(api_url, headers=headers, data=json.dumps(payload))
    if put.status_code in [200, 201]:
        print(f"[GitHub] ✅ 文件已更新: {file_path}")
    else:
        print(f"[GitHub] ❌ 更新失败: {put.text}")


# ===================== 主流程 ===================== #
def main():
    txt = requests.get(IPTV_TXT_URL, timeout=15).text
    m3u = requests.get(IPTV_M3U_URL, timeout=15).text

    for group_name, query in GROUP_QUERIES.items():
        print(f"\n=== 处理分组 {group_name} ===")
        ips = query_fofa(query)
        ips = list(dict.fromkeys(ips))  # 去重
        valid_ip = get_first_valid_ip(ips)
        if valid_ip:
            print(f"[{group_name}] ✅ 使用 IP: {valid_ip}")
        else:
            print(f"[{group_name}] ❌ 无有效IP，标记为失效")
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
