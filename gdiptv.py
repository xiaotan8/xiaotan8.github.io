import requests
import re
import cv2  # 导入OpenCV库
import datetime

#取时间
now = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime('[%m/%d %H:%M]Updated.')
# 定义组播地址和端口 
urls_udp = "/udp/239.77.0.1:5146"
# 定义fofa链接
fofa_url = 'https://fofa.info/result?qbase64=InVkcHh5IiAmJiBwcm90b2NvbD0iaHR0cCIgJiYgY2l0eT0iR3Vhbmd6aG91IiAmJiBzZXJ2ZXI9PSJ1ZHB4eSAxLjAtMjUuMCAocHJvZCkgc3RhbmRhcmQgW0xpbnV4IDUuMTAuMTk0IHg4Nl82NF0i'
fofa_url_jm = 'https://fofa.info/result?qbase64=InVkcHh5IiAmJiBwcm90b2NvbD0iaHR0cCIgJiYgY2l0eT0iSmlhbmdtZW4iICYmIHNlcnZlcj09InVkcHh5IDEuMC0yNS4wIChwcm9kKSBzdGFuZGFyZCBbTGludXggNS4xMC4xOTQgeDg2XzY0XSI%3D'
fofa_url_fs = 'https://fofa.info/result?qbase64=InVkcHh5IiAmJiBwcm90b2NvbD0iaHR0cCIgJiYgY2l0eT0iRm9zaGFuIiAmJiBzZXJ2ZXI9PSJ1ZHB4eSAxLjAtMjUuMCAocHJvZCkgc3RhbmRhcmQgW0xpbnV4IDUuMTAuMTk0IHg4Nl82NF0i'
fofa_url_mz = 'https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjaXR5PSJTaGVuemhlbiIgJiYgc2VydmVyPT0idWRweHkgMS4wLTI1LjAgKHByb2QpIHN0YW5kYXJkIFtMaW51eCA1LjEwLjE5NCB4ODZfNjRdIg=='

# 尝试从fofa链接提取IP地址和端口号，并去除重复项
def extract_unique_ip_ports(fofa_url):
    try:
        response = requests.get(fofa_url)
        html_content = response.text
        # 使用正则表达式匹配IP地址和端口号
        middle = re.findall(r'Array.*</script>', html_content)
        
        ips_ports = re.findall(r'(\d+\.\d+\.\d+\.\d+:\d+)',middle[0])
        return ips_ports if ips_ports else None
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        return None

# 检查视频流的可达性
def check_video_stream_connectivity(ip_port, urls_udp):
    try:
        # 构造完整的视频URL
        video_url = f"http://{ip_port}{urls_udp}"
        # 用OpenCV读取视频
        cap = cv2.VideoCapture(video_url)
        cap2 = cv2.VideoCapture(f"http://{ip_port}/udp/239.77.0.112:5146")
        # 检查视频是否成功打开
        if not cap.isOpened():
            print(f"视频URL：{video_url} 无效")
            return None
        else:
            # 获取视频帧率
            fps = cap.get(cv2.CAP_PROP_FPS)
            fps2 = cap2.get(cv2.CAP_PROP_FPS)
            # 读取视频的宽度和高度
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            print(f"视频URL：{video_url} 的分辨率为 {width}x{height}","[广东珠江]帧率: {:.2f}".format(fps),"[广东体育]帧率: {:.2f}".format(fps2))
            # 检查分辨率是否大于0
            if width > 0 and height > 0 and fps < 40 and fps2 < 40:
                return ip_port  # 返回有效的IP和端口
            # 关闭视频流
            cap.release()
    except Exception as e:
        print(f"访问 {ip_port} 失败: {e}")
    return None

# 更新文件中的IP地址和端口号
def update_files(accessible_ip_port,ip_port_pattern,ip_port_repl):
    global updated_content
    global updated_content_3
    group = re.findall('A|E|J|B',ip_port_pattern)[0]
    #for file_info in files_to_update:
    try:
         # 读取原始文件内容
        response = requests.get('https://xiaotan8.github.io/gdiptv.txt')
        if updated_content:
            file_content = updated_content
        else:
            file_content = response.text
        # 替换文件中的IP地址和端口号
        updated_content = re.sub(ip_port_pattern, ip_port_repl, file_content)
        updated_content = re.sub(r'\[\d+\/\d+ \d+\:\d+\]Updated\.', now, updated_content)
        #失效标记
        if ip_port_repl == '88.88.88.88:8888':
            updated_content = re.sub(f'频道.?{group}(失效|)',f'频道[{group}失效', updated_content)
        else:
            updated_content = re.sub(f'频道.?{group}(失效|)',f'频道[{group}', updated_content)
        # 保存更新后的内容到新文件
        with open('gdiptv.txt', 'w', encoding='utf-8') as file:
            file.write(updated_content)
        print(f"{group}：文件gdiptv.txt已更新并保存。")
    except requests.RequestException as e:
        print(f"无法更新文件gdiptv.txt，错误: {e}")
        
    try:
         # 读取原始文件内容
        response = requests.get('https://xiaotan8.github.io/gdiptv.m3u')
        if updated_content_3:
            file_content = updated_content_3
        else:
            file_content = response.text
        # 替换文件中的IP地址和端口号
        updated_content_3 = re.sub(ip_port_pattern, ip_port_repl, file_content)
        updated_content_3 = re.sub(r'\[\d+\/\d+ \d+\:\d+\]Updated\.', now, updated_content_3)
        #失效标记
        if ip_port_repl == '88.88.88.88:8888':
            updated_content_3 = re.sub(f'频道.?{group}(失效|)',f'频道[{group}失效', updated_content_3)
        else:
            updated_content_3 = re.sub(f'频道.?{group}(失效|)',f'频道[{group}', updated_content_3)
        # 保存更新后的内容到新文件
        with open('gdiptv.m3u', 'w', encoding='utf-8') as file:
            file.write(updated_content_3)
        print(f"{group}：文件gdiptv.m3u已更新并保存。")
    except requests.RequestException as e:
        print(f"无法更新文件gdiptv.m3u，错误: {e}")

def findtheone(unique_ips_ports):
    if unique_ips_ports:
        print("提取到的唯一IP地址和端口号：")
        for ip_port in unique_ips_ports:
            print(ip_port)
    
    # 测试每个IP地址和端口号，直到找到一个可访问的视频流
        valid_ip = None
        for ip_port in unique_ips_ports:
            valid_ip = check_video_stream_connectivity(ip_port, urls_udp)
            if valid_ip:
                break  # 找到有效的IP后，不再继续循环

        if valid_ip:
            print(f"找到可访问的视频流服务: {valid_ip}")

        else:
            valid_ip = '88.88.88.88:8888'
            print("没有找到可访问的视频流服务。")
    else:
        print("没有提取到IP地址和端口号。")
    return valid_ip


# 提取唯一的IP地址和端口号

# 定义需要更新的文件列表
files_to_update = [
    {'url': 'https://xiaotan8.github.io/gdiptv.txt', 'filename': 'gdiptv.txt'}
]

#定义正则
ip_port_pattern = r'((?<=\[A\](\,|\n)http://)\d+\.\d+\.\d+\.\d+:\d+)'
ip_port_pattern_fs = r'((?<=\[E\](\,|\n)http://)\d+\.\d+\.\d+\.\d+:\d+)'
ip_port_pattern_jm = r'((?<=\[J\](\,|\n)http://)\d+\.\d+\.\d+\.\d+:\d+)'
ip_port_pattern_mz = r'((?<=\[B\](\,|\n)http://)\d+\.\d+\.\d+\.\d+:\d+)'





# 更新文件中的IP地址和端口号
updated_content = ''
updated_content_3 = ''
try:
    unique_ips_ports = extract_unique_ip_ports(fofa_url)
    print(unique_ips_ports)
    valid_ip = findtheone(unique_ips_ports)
    ip_port_repl = valid_ip
    print(valid_ip)
    update_files(valid_ip,ip_port_pattern,ip_port_repl)
except requests.RequestException as e:
    print(f"错误: {e}")
try:
    unique_ips_ports_fs = extract_unique_ip_ports(fofa_url_fs)
    print(unique_ips_ports_fs)
    valid_ip_fs = findtheone(unique_ips_ports_fs)
    ip_port_repl_fs = valid_ip_fs
    print(valid_ip_fs)
    update_files(valid_ip_fs,ip_port_pattern_fs,ip_port_repl_fs)
except requests.RequestException as e:
    print(f"错误: {e}")
try:
    unique_ips_ports_jm = extract_unique_ip_ports(fofa_url_jm)
    print(unique_ips_ports_jm)
    valid_ip_jm = findtheone(unique_ips_ports_jm)
    ip_port_repl_jm = valid_ip_jm
    print(valid_ip_jm)
    update_files(valid_ip_jm,ip_port_pattern_jm,ip_port_repl_jm)
except requests.RequestException as e:
    print(f"错误: {e}")
try:
    unique_ips_ports_mz = extract_unique_ip_ports(fofa_url_mz)
    print(unique_ips_ports_mz)
    valid_ip_mz = findtheone(unique_ips_ports_mz)
    ip_port_repl_mz = valid_ip_mz
    print(valid_ip_mz)
    update_files(valid_ip_mz,ip_port_pattern_mz,ip_port_repl_mz)
except requests.RequestException as e:
    print(f"错误: {e}")
