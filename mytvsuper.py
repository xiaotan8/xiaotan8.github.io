import requests

CHANNEL_LIST = {
    'JUHD': {
        'name': '翡翠台(超高清)',
        'license': '2c045f5adb26d391cc41cd01f00416fa:fc146771a9b096fc4cb57ffe769861be',
        'logo': 'https://assets.livednow.com/logo/翡翠台.png'
    },
    'J': {
        'name': '翡翠台',
        'license': '0958b9c657622c465a6205eb2252b8ed:2d2fd7b1661b1e28de38268872b48480',
        'logo': 'https://assets.livednow.com/logo/翡翠台.png'
    },
    'P': {
        'name': '明珠台',
        'license': 'e04facdd91354deee318c674993b74c1:8f97a629de680af93a652c3102b65898',
        'logo': 'https://assets.livednow.com/logo/明珠台.png'
    },
    'B': {
        'name': 'TVB Plus',
        'license': '56603b65fa1d7383b6ef0e73b9ae69fa:5d9d8e957d2e45d8189a56fe8665aaaa',
        'logo': 'https://img.sky4k.top/TVB_Plus_CheerVisionTV.png'
    },
    'C': {
        'name': '無線新聞台',
        'license': '90a0bd01d9f6cbb39839cd9b68fc26bc:51546d1f2af0547f0e961995b60a32a1',
        'logo': 'https://assets.livednow.com/logo/無線新聞台.png'
    },
    'CWIN': {
        'name': 'myTV SUPER FREE',
        'license': '0737b75ee8906c00bb7bb8f666da72a0:15f515458cdb5107452f943a111cbe89',
        'logo': 'https://assets.livednow.com/logo/MytvSuper.png'
    },
    'C18': {
        'name': 'myTV SUPER 18台',
        'license': '72de7d0a1850c8d40c5bdf9747a4ca7c:4967537ff0bc8209277160759de4adef',
        'logo': 'https://assets.livednow.com/logo/myTV-SUPER-18.png'
    },
    'TVG': {
        'name': '黃金翡翠台',
        'license': '8fe3db1a24969694ae3447f26473eb9f:5cce95833568b9e322f17c61387b306f',
        'logo': 'https://assets.livednow.com/logo/黃金翡翠台.png'
    },
    'CTVC': {
        'name': '千禧經典台',
        'license': '6c308490b3198b62a988917253653692:660578b8966fe8012ad51b9aae7a5d78',
        'logo': 'https://assets.livednow.com/logo/千禧經典台.png'
    },
    'CDR3': {
        'name': '華語劇台',
        'license': 'baae227b5fc06e2545868d4a1c9ced14:8cd460458b0bdecca5c12791b6409278',
        'logo': 'https://assets.livednow.com/logo/華語劇台.png'
    },
    'CCLM': {
        'name': '粵語片台',
        'license': '5b90da7fd2f018bf85a757241075626f:75c0897b4cf5ce154ddae86eddb79cd3',
        'logo': 'https://assets.livednow.com/logo/粵語片台.png'
    },
    'CTVS': {
        'name': '亞洲劇台',
        'license': 'df5c0e617dffc3e3c44cb733dccb33c0:7d00ec9cd4f54d5baf94c03edc8cfe25',
        'logo': 'https://assets.livednow.com/logo/亞洲劇台.png'
    },
    'TVO': {
        'name': '黃金華劇台',
        'license': 'acd93a5f665efd4feadb26f5ed48fd96:c6ce58ef9cce30638e0c2e9fc45a6dbd',
        'logo': 'https://assets.livednow.com/logo/黃金華劇台.png'
    },
    'CTVE': {
        'name': '娛樂新聞台',
        'license': '6fa0e47750b5e2fb6adf9b9a0ac431a3:a256220e6c2beaa82f4ca5fba4ec1f95',
        'logo': 'https://assets.livednow.com/logo/娛樂新聞台.png'
    },
    'CCOC': {
        'name': '戲曲台',
        'license': 'c91c296ef6c46b3f2af1da257553bd17:d6e92d5e594f6f8e494a6e1c9df75298',
        'logo': 'https://assets.livednow.com/logo/戲曲台.png'
    },
    'KID': {
        'name': 'SUPER Kids Channel',
        'license': '42527ca90ad525ba2eac9979c93d3bca:b730006ad1da48b412ceb1f9e36a833d',
        'logo': 'https://assets.livednow.com/logo/SUPER-Kids-Channel.png'
    },
    'ZOO': {
        'name': 'ZooMoo',
        'license': '9c302eb50bef5a9589d97cb90982b05e:2603e646caafe22bc4e8a17b5a2dd55b',
        'logo': 'https://assets.livednow.com/logo/ZooMoo.png'
    },
    'CNIKO': {
        'name': 'Nickelodeon',
        'license': '0e69430290ed7b00af4db78419dcad8b:e4769b57a66e8e9737d6d86f317600c0',
        'logo': 'https://assets.livednow.com/logo/Nickelodeon.png'
    },
    'CNIJR': {
        'name': 'Nick Jr.',
        'license': '9f1385d2a12a67b572b9d968eb850337:3086bcd49a909606a8686858c05c7e33',
        'logo': 'https://assets.livednow.com/logo/Nick-Jr..png'
    },
    'CMAM': {
        'name': '美亞電影台',
        'license': 'c5d6f2afbd6b276312b0471a653828e1:ecbbb4a3ffa2200ae69058e20e71e91b',
        'logo': 'https://assets.livednow.com/logo/美亞電影台-HK.png'
    },
    'CTHR': {
        'name': 'Thrill',
        'license': 'b22355363ab2b09a6def54be0c89b9f2:4b196c2bf24b37e82a81031246de6efe',
        'logo': 'https://assets.livednow.com/logo/Thrill.png'
    },
    'CCCM': {
        'name': '天映經典頻道',
        'license': '627b6ca150887912bec47ae4a9b85269:2bf49b2105d20544a6db89c0577b9802',
        'logo': 'https://assets.livednow.com/logo/天映經典頻道.png'
    },
    'CMC': {
        'name': '中國電影頻道',
        'license': 'cabb16d20e71b512f24e9ece0cb09396:2d43505980a22014ee1a476880982308',
        'logo': 'https://assets.livednow.com/logo/中國電影頻道.png'
    },
    'CRTX': {
        'name': 'ROCK Action',
        'license': '358eacad1f06e8e375493dabee96d865:461a02b2eb1232c6c100b95bd0bf40f8',
        'logo': 'https://assets.livednow.com/logo/Rock-Action-HK.png'
    },
    'CKIX': {
        'name': 'KIX',
        'license': '3b4a44c5ef3217c55a357ad976d328b2:f3355e5a30722e631031b851642c27f1',
        'logo': 'https://assets.livednow.com/logo/KIX.png'
    },
    'LNH': {
        'name': 'Love Nature HD',
        'license': '03fb0f439f942f50d06bf23a511bf4f8:bae7115da07195263e50ae5fc8bbe4f3',
        'logo': 'https://assets.livednow.com/logo/Love-Nature-HK.png'
    },
    'LN4': {
        'name': 'Love Nature 4K',
        'license': '037c644cb92137ac5c8d653e952e4c8f:b3b2fcbe576a63cf3bbb9425da3de4cf',
        'logo': 'https://assets.livednow.com/logo/Love-Nature-4K-HK.png'
    },
    'SMS': {
        'name': 'Global Trekker',
        'license': 'a8f381c2a3114cc6c55f50b6ff0c78f3:86922e5993788488e1eca857c00d4fab',
        'logo': 'https://assets.livednow.com/logo/Global-Trekker-HK.png'
    },
    'CRTE': {
        'name': 'ROCK 綜藝娛樂',
        'license': '002d034731b6ac938ea7ba85bc3dc759:6694258c023d73492a10acb860bc6161',
        'logo': 'https://assets.livednow.com/logo/Rock-Entertainment-HK.png'
    },
    'CAXN': {
        'name': 'AXN',
        'license': '20bea0e14af0d3dcb63d4126e8b50172:07382de357a2b0cceabe82e0b37cb8de',
        'logo': 'https://assets.livednow.com/logo/AXN.png'
    },
    'CANI': {
        'name': 'Animax',
        'license': 'b1a073dbd8272b0c99940db624ce8d74:9fec26ff4c6774a8bde881e5cb0fe82e',
        'logo': 'https://assets.livednow.com/logo/Animax-HK.png'
    },
    'CJTV': {
        'name': 'tvN',
        'license': 'adcab9e8e5644ff35f04e4035cc6ad3b:d8e879e108a96fde6537c1b679c369b5',
        'logo': 'https://assets.livednow.com/logo/tvN-HK.png'
    },
    'CTS1': {
        'name': '無線衛星亞洲台',
        'license': 'ad7b06658e8a36a06def6b3550bde35c:b672f89570a630abb1d2abb5030e6303',
        'logo': 'https://assets.livednow.com/logo/無線衛星亞洲台.png'
    },
    'CRE': {
        'name': '創世電視',
        'license': 'adef00c5ba927d01642b1e6f3cedc9fb:b45d912fec43b5bbd418ea7ea1fbcb60',
        'logo': 'https://xiaotan.860775.xyz/創世電視.png'
    },
    'FBX': {
        'name': 'FashionBox',
        'license': '4df52671ef55d2a7ac03db75e9bba2f7:4a3c16e8098c5021f32c7d4f66122477',
        'logo': 'https://assets.livednow.com/logo/FashionBox.png'
    },
    'CMEZ': {
        'name': 'Mezzo Live HD',
        'license': 'e46f2747a9cf6822a608786bbc21d400:d8778fcf92c949e949a6700828f5f67e',
        'logo': 'https://assets.livednow.com/logo/Mezzo-Live-HK.png'
    },
    'DTV': {
        'name': '東方衛視國際頻道',
        'license': '9d6a139158dd1fcd807d1cfc8667e965:f643ba9204ebba7a5ffd3970cfbc794c',
        'logo': 'https://assets.livednow.com/logo/東方衛視國際頻道.png'
    },
    'PCC': {
        'name': '鳳凰衛視中文台',
        'license': '7bca0771ba9205edb5d467ce2fdf0162:eb19c7e3cea34dc90645e33f983b15ab',
        'logo': 'https://assets.livednow.com/logo/鳳凰中文.png'
    },
    'PIN': {
        'name': '鳳凰衛視資訊台',
        'license': '83f7d313adfc0a5b978b9efa0421ce25:ecdc8065a46287bfb58e9f765e4eec2b',
        'logo': 'https://assets.livednow.com/logo/鳳凰資訊.png'
    },
    'PHK': {
        'name': '鳳凰衛視香港台',
        'license': 'cde62e1056eb3615dab7a3efd83f5eb4:b8685fbecf772e64154630829cf330a3',
        'logo': 'https://assets.livednow.com/logo/鳳凰香港.png'
    },
    'POPC': {
        'name': 'PopC',
        'license': '221591babff135a71961d09399d2c922:c80ca4c7b801a76a07179dfb7debb57d',
        'logo': 'https://assets.livednow.com/logo/PopC.png'
    },
    'CC1': {
        'name': '中央電視台綜合頻道 (港澳版)',
        'license': 'e50b18fee7cab76b9f2822e2ade8773a:2e2e8602b6d835ccf10ee56a9a7d91a2',
        'logo': 'https://assets.livednow.com/logo/中央電視台綜合頻道-港澳版.png'
    },
    'CGD': {
        'name': 'CGTN (中國環球電視網)記錄頻道',
        'license': 'b570ae67cb063428b158eb2f91c6d77c:c573dabca79a17f81755c0d4b33384bc',
        'logo': 'https://assets.livednow.com/logo/中國環球電視網-記錄頻道.png'
    },
    'CGE': {
        'name': 'CGTN (中國環球電視網)英語頻道',
        'license': '4331903278b673916cc6940a8b8d9e7e:02a409115819de9acd9e907b053e3aa8',
        'logo': 'https://assets.livednow.com/logo/中國環球電視網-英語頻道.png'
    },
    'CMN1': {
        'name': '神州新聞台',
        'license': '7ee6ed08925f4716c8d0943e7bdb3e5f:6f3c1e31b30ccac36d466f41489ceb27',
        'logo': 'https://assets.livednow.com/logo/神州新聞台.png'
    },
    'CTSN': {
        'name': '無線衛星新聞台',
        'license': '73aaeb9e84db423627018017059e0f9d:34148a56250459383f7ef7369073bf39',
        'logo': 'https://assets.livednow.com/logo/無線衛星新聞台.png'
    },
    'CCNA': {
        'name': '亞洲新聞台',
        'license': 'ddc7bb2603628134334919a0d7327d1d:a5fcd8bb852371faedd13b684f5adede',
        'logo': 'https://assets.livednow.com/logo/亞洲新聞台.png'
    },
    'CJAZ': {
        'name': '半島電視台英語頻道',
        'license': '80c76105d3ae35dfe25f939d1fb83383:6d76e7ba039773bced47d78e6de4fcf0',
        'logo': 'https://assets.livednow.com/logo/半島電視台英語頻道.png'
    },
    'CF24': {
        'name': 'France 24',
        'license': '2d4f6b8755a918d2126a2ee78791cf0b:c392acc1a1a070d2bcdf518d99d88406',
                'logo': 'https://assets.livednow.com/logo/France-24-HK.png'
    },
    'CDW1': {
        'name': 'DW',
        'license': '2bb557c09dfc01a27ab81778913f2a10:d00ca6eb9a83ffde846324109fb445ba',
        'logo': 'https://assets.livednow.com/logo/DW-HK.png'
    },
    'CNHK': {
        'name': 'NHK World-Japan',
        'license': '71e0189622e045c3d2600022de82e1a1:1b4bfeeb0a88d29af064fe8017f1e238',
        'logo': 'https://assets.livednow.com/logo/NHK-HK.png'
    },
    'CARI': {
        'name': 'Arirang TV',
        'license': 'fddbd3771eac81f4e293fb2a982bf53e:ee83f18204accf860fc59cee3fde61d2',
        'logo': 'https://assets.livednow.com/logo/Arirang-HK.png'
    },
    'EVT1': {
        'name': 'myTV SUPER 直播足球1台',
        'license': 'e8ca7903e25450d85cb32b3057948522:d5db5c03608f5f6c8a382c6abcb829e4',
        'logo': 'https://assets.livednow.com/logo/MytvSuper.png'
    },
    'EVT2': {
        'name': 'myTV SUPER 直播足球2台',
        'license': '024f2733fb9afad23490149c601ce47c:034db34d56263c79c7f41448f2a6cfc1',
        'logo': 'https://assets.livednow.com/logo/MytvSuper.png'
    },
    'EVT3': {
        'name': 'myTV SUPER 直播足球3台',
        'license': 'fddbd3771eac81f4e293fb2a982bf53e:ee83f18204accf860fc59cee3fde61d2',
        'logo': 'https://assets.livednow.com/logo/MytvSuper.png'
    },
    'EVT4': {
        'name': 'myTV SUPER 直播足球4台',
        'license': '91bb59ef653df8bf0cb39dfb6217277f:2a22ec32c64add9cec2b18442f507abc',
        'logo': 'https://assets.livednow.com/logo/MytvSuper.png'
    },
    'EVT5': {
        'name': 'myTV SUPER 直播足球5台',
        'license': 'cc36cf8acc9e1510c38cd6cceae92175:2e0e1c3774a3e1bba5771eaf37c0ab36',
        'logo': 'https://assets.livednow.com/logo/MytvSuper.png'
    },
    'EVT6': {
        'name': 'myTV SUPER 直播足球6台',
        'license': 'e069fc056280e4caa7d0ffb99024c05a:d3693103f232f28b4781bbc7e499c43a',
        'logo': 'https://assets.livednow.com/logo/MytvSuper.png'
    }
}

def get_mytvsuper(channel):
    if channel not in CHANNEL_LIST:
        return '频道代号错误'

    api_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJib3NzX2lkIjoiNzE5NTY4NDQ5IiwiZGV2aWNlX3Rva2VuIjoick1WS0xGVDNLUHRBdG1TSHJFcFBVWXFTIiwiZGV2aWNlX2lkIjoiTW1VNU9EQXhaVEV0WW1Ga1ppMDBNekZtTFdFeE5UZ3RNek16WW1ObU5HVmxPV1ppIiwiZGV2aWNlX3R5cGUiOiJ3ZWIiLCJkZXZpY2Vfb3MiOiJicm93c2VyIiwiZHJtX2lkIjoiTW1VNU9EQXhaVEV0WW1Ga1ppMDBNekZtTFdFeE5UZ3RNek16WW1ObU5HVmxPV1ppIiwiZXh0cmEiOnsicHJvZmlsZV9pZCI6MX0sImlhdCI6MTcyMDMyODAyNSwiZXhwIjoxNzIwMzMxNjI1fQ.arkZVqB_0064Z4tdg100L2IQXGjzykM8Yzuy2NT5TIk0PM9raA3ns0kiM7PUkV5JhssqDql0bTCjI3lt-8wvCbE3EkApbjZMo3X-LzzlQ23n5AG7TlXjckdU-_3jYKfe9d3syjz9oxleKlfWReG8t6nXv4I8_RAYPxiDSDsIsnuAhMFzaRFuUkK2AThm2F5g0nY_1l8dKuV6L6GdEoABxQb2RVEFEgqRQqoLvpI8gHfwhPsF0NuI9opR7gVmJXlLOmr7SJ_hwQuj5_YrFr5Zr42Vit2JS-Sp1_sbkr_yUSJeM1aPYEOCM7pPQpnDGTbY_S5-5wGZnlxZ1-jAWPJno1A2e4mVcDFDzClhaiWSYvWUTSm4MIk1ssjOWSivK_jemXmhtLkUnNmyS0LZPxpqNzQB9iEbUpd1y304xrkNFl-axhwH3XIA3ToUtxDXNXfglEMqt0FXPlhE9b0HqvxumpuFUvg9ObMB4G8n2ovWKQ9iJ1nO4_fGf4sgtpONru0aPWYvKgNKxS9HY0o6ZCl5oaMRplxla9z_3Mx-eu735CCfrsd-CtizEBMNYvlfrDNJe0uhSFiW0pgaaPtLG4enEq6CPnvFSQBm18xXRRsz9g6epw-nXb6A652m7IGTeLAj_YimKVPpMo9M3tjusYbwYY6Vv3YOyFfl8ZQJJjhymmY'  # Replace with your actual API token
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + api_token,
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Host': 'user-api.mytvsuper.com',
        'Origin': 'https://www.mytvsuper.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.2 Safari/605.1.15',
        'Referer': 'https://www.mytvsuper.com/',
        'X-Forwarded-For': '210.6.4.148'  # 香港原生IP  210.6.4.148
    }

    params = {
        'platform': 'android_tv',
        'network_code': channel
    }

    url = 'https://user-api.mytvsuper.com/v1/channel/checkout'
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        return '请求失败'

    response_json = response.json()
    profiles = response_json.get('profiles', [])

    play_url = ''
    for profile in profiles:
        if profile.get('quality') == 'high':
            play_url = profile.get('streaming_path', '')
            break

    if not play_url:
        return '未找到播放地址'

    play_url = play_url.split('&p=')[0]

    license_key = CHANNEL_LIST[channel]['license']
    channel_name = CHANNEL_LIST[channel]['name']
    channel_logo = CHANNEL_LIST[channel]['logo']
    m3u_content = f"#EXTINF:-1 tvg-id=\"{channel}\" tvg-name=\"{channel_name}\" tvg-logo=\"{channel_logo}\",{channel_name}\n"
    m3u_content += "#KODIPROP:inputstream.adaptive.manifest_type=mpd\n"
    m3u_content += "#KODIPROP:inputstream.adaptive.license_type=clearkey\n"
    m3u_content += f"#KODIPROP:inputstream.adaptive.license_key=https://h2j.860775.xyz/{license_key}\n"
    m3u_content += f"{play_url}\n"

    return m3u_content

# 创建或打开文件用于写入
with open('mytvsuper.m3u', 'w', encoding='utf-8') as m3u_file:
    # 写入 M3U 文件的头部
    m3u_file.write("#EXTM3U url-tvg=\"https://xmltv.bph.workers.dev\"\n")

    # 遍历所有频道并写入每个频道的 M3U 内容
    for channel_code in CHANNEL_LIST.keys():
        m3u_content = get_mytvsuper(channel_code)
        m3u_file.write(m3u_content)

print("所有频道的 M3U 播放列表已生成并保存为 'mytvsuper.m3u'。")
