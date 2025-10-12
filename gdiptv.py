import requests
import re
import cv2
import datetime
import concurrent.futures
import os
import json
import base64
import urllib.parse

# --- 全局配置 ---
# 请将您的 FOFA API Token 填写在这里
# 获取方式：登录 FOFA -> 用户中心 -> 我的 API Token
FOFA_API_KEY = "b3f3d61ce850e02076fec41f70a203f6" 

# --- 全局常量 ---
now = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime('[%m/%d %H:%M]Updated.')
VERIFY_UDP_PATH = "/udp/239.77.0.1:5146"
TEST_UDP_PATH = "/udp/239.77.0.112:5146"

# 远程文件 URL (您的 GitHub Pages 文件)
REMOTE_TXT_URL = "https://xiaotan8.github.io/gdiptv.txt"
REMOTE_M3U_URL = "https://xiaotan8.github.io/gdiptv.m3u"

# 用于在播放列表中匹配和替换旧IP的正则表达式
# 这个正则会匹配以 http:// 开头的 IP:PORT
UNIFIED_IP_PATTERN = r"http://(\d+\.\d+\.\d+\.\d+:\d+)"


def get_ips_from_fofa_by_api(query, group_name):
    """
    使用 FOFA API 查询服务器列表。
    使用 FOFA 官方推荐的编码方式: base64(urlencode(query))
    
    Args:
        query (str): FOFA 查询语句
        group_name (str): 分组名称，用于日志打印
    
    Returns:
        list: 唯一的 IP:Port 列表。
    """
    print(f"\n--- 正在查询 [{group_name}] 的 IP ---")
    print(f"查询语句: {query}")

    if not FOFA_API_KEY or FOFA_API_KEY == "YOUR_FOFA_API_KEY_HERE":
        print("  [错误] 请先在脚本顶部配置您的 FOFA_API_KEY！")
        return []

    # 1. 将查询语句编码为字节流 (UTF-8)
    query_bytes = query.encode('utf-8')
    
    # 2. 对字节流进行 URL 编码
    encoded_query_bytes = urllib.parse.quote_plus(query_bytes)
    
    # 3. 将 URL 编码后的字节流进行 Base64 编码
    #    注意：FOFA 的 qbase64 参数是 Base64 编码的 URL 编码字符串
    qbase64_value = base64.b64encode(encoded_query_bytes).decode('utf-8')
    
    # 4. 构建最终的 API URL
    #    注意：API 参数是 email，不是 key
    api_url = f"https://fofa.info/api/v1/search/all?email={FOFA_API_KEY}&qbase64={qbase64_value}&size=500"
    
    print(f"  [调试] 构造的API URL (Key已隐藏): {api_url.replace(FOFA_API_KEY, 'YOUR_API_KEY')}")

    try:
        # 添加一个 User-Agent，模拟浏览器请求，避免被一些严格的防火墙拦截
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(api_url, headers=headers, timeout=20)
        response.raise_for_status()
        result_data = response.json()
        
        if "error" in result_data and result_data["error"]:
            print(f"  [错误] FOFA API 返回错误: {result_data.get("errmsg", "未知错误")}")
            return []

        ips_ports = set()
        results = result_data.get("results", [])
        if not results:
             print(f"  [信息] 查询成功，但未返回结果。")
                 return []

        for item in results:
            if isinstance(item, list) and len(item) > 0 and isinstance(item[0], str):
                ip_port_match = re.match(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+)", item[0])
                if ip_port_match:
                    ips_ports.add(ip_port_match.group(1))

        if not ips_ports:
            print(f"  [信息] 未提取到有效的 IP:Port 格式。")
            return []
                
        unique_ips = sorted(list(ips_ports))
        print(f"  [成功] 共查询到 {len(unique_ips)} 个 IP。")
        return unique_ips

    except requests.exceptions.RequestException as e:
        print(f"  [错误] 请求 FOFA API 失败: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"  [错误] 解析 JSON 数据失败: {e}")
        return []


def find_valid_ip(ip_list):
    """使用多线程验证IP列表，返回第一个有效的IP。"""
    print(f"--- 开始验证，共 {len(ip_list)} 个IP待验证 ---")
    final_valid_ip = "88.88.88.88:8888" # 默认值
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        futures = [executor.submit(verify_single_ip, ip_port) for ip_port in ip_list]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                print(f"  [成功] 找到有效IP: {result}")
                return result # 找到即返回
    print(f"--- 验证结束，未找到有效IP ---")
    return final_valid_ip # 所有IP都验证失败后返回默认值


def verify_single_ip(ip_port):
    """验证单个IP地址的视频流是否有效。"""
    verify_url = f"http://{ip_port}{VERIFY_UDP_PATH}"
    test_url = f"http://{ip_port}{TEST_UDP_PATH}"
    
    cap_verify = None
    cap_test = None
    try:
        cap_verify = cv2.VideoCapture(verify_url)
        if not cap_verify.isOpened() or not cap_verify.read()[0]:
            return None

        cap_test = cv2.VideoCapture(test_url)
        if not cap_test.isOpened():
            return None

        fps = cap_test.get(cv2.CAP_PROP_FPS)
        if fps <= 0 or fps >= 40:
            return None
            
        return ip_port
    except Exception:
        return None
    finally:
        if cap_verify: cap_verify.release()
        if cap_test: cap_test.release()

def update_playlist_files(valid_ip):
    """
    使用找到的有效 IP 更新本地播放列表文件。
    """
    print(f"\n--- 正在使用有效 IP: {valid_ip} 更新播放列表文件 ---")

    content_txt = get_remote_file_content(REMOTE_TXT_URL)
    content_m3u = get_remote_file_content(REMOTE_M3U_URL)
    
    if not content_txt or not content_m3u:
        print("  [错误] 无法获取远程文件内容，更新中止。")
        return

    # 统一替换所有旧IP为新的有效IP
    # 使用 g<1> 保留原始的 http:// 部分
    new_ip_str = f"http://{valid_ip}"
    updated_content_txt = re.sub(UNIFIED_IP_PATTERN, new_ip_str, content_txt)
    updated_content_m3u = re.sub(UNIFIED_IP_PATTERN, new_ip_str, content_m3u)
    
    # 替换更新时间
    updated_content_txt = re.sub(r"\[\d+\/\d+ \d+\:\d+\]Updated\.", now, updated_content_txt)
    updated_content_m3u = re.sub(r"\[\d+\/\d+ \d+\:\d+\]Updated\.", now, updated_content_m3u)
    
    # 统一更新所有频道的状态为正常
    status_suffix = "正常" # 找到了IP，所以是正常
    channel_status_pattern = re.compile(r"频道\[([^\]]+)\][^,\n]*")
    updated_content_txt = channel_status_pattern.sub(f"频道[\\1]{status_suffix}", updated_content_txt)
    updated_content_m3u = channel_status_pattern.sub(f"频道[\\1]{status_suffix}", updated_content_m3u)

    # 保存文件
    filenames = ["gdiptv.txt", "gdiptv.m3u"]
    contents = [updated_content_txt, updated_content_m3u]

    for filename, content in zip(filenames, contents):
        if not content:
            continue
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  [成功] 文件 {filename} 已更新。")
        except IOError as e:
            print(f"  [错误] 保存文件 {filename} 失败: {e}")

def get_remote_file_content(url):
    """从远程URL获取文件内容。"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException:
        return None


# --- 新的 IP 任务组配置 ---
# 定义多个查询组来获取不同地区的IP，以提高成功率。
# "name": 分组名称
# "query": FOFA API 的查询语句
IP_GROUPS = [
    {
        "name": "广州-电信",
        "query": '"udpxy" && protocol="http" && region="Guangzhou" && org="Chinanet"'
    },
    {
        "name": "广州-联通",
        "query": '"udpxy" && protocol="http" && region="Guangzhou" && org="ChinaUnicom"'
    },
    {
        "name": "深圳-电信",
        "query": '"udpxy" && protocol="http" && region="Shenzhen" && org="Chinanet"'
    },
    {
        "name": "深圳-联通",
        "query": '"udpxy" && protocol="http" && region="Shenzhen" && org="ChinaUnicom"'
    },
    {
        "name": "佛山-电信",
        "query": '"udpxy" && protocol="http" && region="Foshan" && org="Chinanet"'
    },
    {
        "name": "东莞-电信",
        "query": '"udpxy" && protocol="http" && region="Dongguan" && org="Chinanet"'
    },
    # 您可以根据需要任意添加更多的组合，例如珠海、惠州、移动等
]


# --- 主执行逻辑 ---
if __name__ == "__main__":
    print("========== 广东IPTV源自动更新工具 (多分组查询版) ==========")
    print(f"--- 程序启动于 {now} ---")
    print(f"--- 当前工作目录: {os.getcwd()} ---")
    
    # 由于FOFA_KEY已经默认填入，这里的检查可以移除或修改，但保留也无害
    if FOFA_API_KEY == "YOUR_FOFA_API_KEY_HERE":
        print("="*50)
        print("!!! 错误：请先在脚本顶部设置您的 FOFA_API_KEY !!!")
        print("="*50)
        exit(1)

    final_valid_ip = None

    # 遍历所有 IP 任务组，直到找到可用的IP
    for group in IP_GROUPS:
        ips = get_ips_from_fofa_by_api(group["query"], group["name"])

        if not ips:
            continue # 如果当前组没有结果，继续下一个组

        print(f"--- 在 [{group["name"]}] 组中找到了IP，开始验证... ---")
        final_valid_ip = find_valid_ip(ips)
        
        # 如果找到了有效IP，立即跳出循环，不查询后面的组了
        if final_valid_ip and final_valid_ip != "88.88.88.88:8888":
            print(f"--- 在 [{group["name"]}] 组成功找到有效IP，停止查询其他组。 ---")
            break

    print("\n========== IP 查询和验证阶段结束 ==========")

    # 最后，根据找到的IP更新文件
    if final_valid_ip and final_valid_ip != "88.88.88.88:8888":
        update_playlist_files(final_valid_ip)
    else:
        print("  [最终结果] 经过多组查询，未找到任何可用IP。播放列表将不会更新。")
        # 您可以在这里选择将本地文件标记为失效，但此版本不做修改，保持原样。
