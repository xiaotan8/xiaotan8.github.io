import os
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
        'license': '9c2ecde1c31185ab61ed4689b87ae332:54895a656e053a73b39882e7a56d642b',
        'logo': 'https://assets.livednow.com/logo/NHK-HK.png'
    },
    'CARI': {
        'name': 'Arirang TV',
        'license': 'f3ae14e72f585eaf14b18d8d9515d43f:ce0e375c3966263877078aadd815742e',
        'logo': 'https://assets.livednow.com/logo/Arirang-HK.png'
    },
        'ONC': {
        'name': '奧運新聞台',
        'license': '68f99a5e1cc393fb79ed98a2a955cb2b:9fcc81e5f0a1021867d93038b9149c6b',
        'logo': 'https://assets.livednow.com/logo/myTV-SUPER-Olympics-News.png'
    },
    'OL01': {
        'name': '奧運801台',
        'license': '024f2733fb9afad23490149c601ce47c:034db34d56263c79c7f41448f2a6cfc1',
        'logo': 'https://assets.livednow.com/logo/myTV-SUPER-Olympics-1.png'
    },
    'OL02': {
        'name': '奧運802台',
        'license': '69a81a757b16a3d431d4365d81f07f07:292f2fdc2002e8346cd2c18af4a3a4bc',
        'logo': 'https://assets.livednow.com/logo/myTV-SUPER-Olympics-2.png'
    },
    'OL03': {
        'name': '奧運803台',
        'license': '0c79f7330982b6e508de3df47b88fbdc:db063550682430e8ca5857a85ccbc297',
        'logo': 'https://assets.livednow.com/logo/myTV-SUPER-Olympics-3.png'
    },
    'OL04': {
        'name': '奧運804台',
        'license': 'dddcd998a3107f7b350a7536c7fd30b1:15b343513bda8a5816b45295690c3792',
        'logo': 'https://assets.livednow.com/logo/myTV-SUPER-Olympics-4.png'
    },
    'OL05': {
        'name': '奧運805台',
        'license': 'b8d3124914a5cf9c913eccff19d53510:529601f9fca6d76bb429ef2d2bca3622',
        'logo': 'https://assets.livednow.com/logo/myTV-SUPER-Olympics-5.png'
    },
    'OL06': {
        'name': '奧運806台',
        'license': '980d5c8748c494a3c57902a3074e4ed4:76dcab6f98a0d8145b9d25c32fa341c4',
        'logo': 'https://assets.livednow.com/logo/myTV-SUPER-Olympics-6.png'
    },
    'OL07': {
        'name': '奧運807台',
        'license': '316eb6af6ffa7ec2f40b710da9004a52:22733382c3ccff75647e45a3dbf181a8',
        'logo': 'https://assets.livednow.com/logo/myTV-SUPER-Olympics-7.png'
    },
    'OL08': {
        'name': '奧運808台',
        'license': '3ef1880f434fb483d8ef645f5ad0f7b8:dd2c2c71ff8adfea810ebb3c21ec810e',
        'logo': 'https://assets.livednow.com/logo/myTV-SUPER-Olympics-8.png'
    },
    'OL09': {
        'name': '奧運809台',
        'license': '355998163e1753eaa3feb69829095eb3:7e6af588f7fa576621f68103cd41487e',
        'logo': 'https://assets.livednow.com/logo/myTV-SUPER-Olympics-9.png'
    },
    'OL10': {
        'name': '奧運810台',
        'license': 'e1ce1a32fd8716af515eb209ccf6ce4b:fde3579a221cea754f3b1d7ff1958f6c',
        'logo': 'https://assets.livednow.com/logo/myTV-SUPER-Olympics-10.png'
    },
    'OL11': {
        'name': '奧運811台',
        'license': '34a3035c05adfa6719d6f96def57ae94:f3deb53017fdcf91eb198c2e9b9153f4',
        'logo': 'https://assets.livednow.com/logo/myTV-SUPER-Olympics-11.png'
    },
    'OL12': {
        'name': '奧運812台',
        'license': 'e5d411ba4e8221f5c4f75215925f1892:d3794918aaf381203d0c50cf1afdfa15',
        'logo': 'https://assets.livednow.com/logo/myTV-SUPER-Olympics-12.png'
    },
    'OL13': {
        'name': '奧運813台',
        'license': 'c8d8bba7d15614168a2e16641ccec855:dc692afdb5048efb64b87d4edd74bf6b',
        'logo': 'https://assets.livednow.com/logo/myTV-SUPER-Olympics-13.png'
    },
    'OL14': {
        'name': '奧運814台',
        'license': '78703895a6ef7a6e4c9d99fae257d858:be30ea5033e24ff1b9dab7de9f4f5275',
        'logo': 'https://assets.livednow.com/logo/myTV-SUPER-Olympics-14.png'
    },
    'OL15': {
        'name': '奧運815台',
        'license': '0c039e5195e04911444b8e4c00d2f5aa:e6e64ebf658621f013e917dce8b177f6',
        'logo': 'https://assets.livednow.com/logo/myTV-SUPER-Olympics-15.png'
    },
    'OL16': {
        'name': '奧運816台',
        'license': 'd604fae19fcba50a4083a6844c2ca0e7:b46698aef5d28c07fdf5d69724cd6c23',
        'logo': 'https://assets.livednow.com/logo/myTV-SUPER-Olympics-16.png'
    },
    'EVT3': {
        'name': 'myTV SUPER 直播足球3台',
        'license': '84f456002b780253dab5534e9713323c:65aeb769264f41037cec607813e91bae',
        'logo': 'https://assets.livednow.com/logo/MytvSuper.png'
    },
    'EVT4': {
        'name': 'myTV SUPER 直播足球4台',
        'license': '848d6d82c14ffd12adf4a7b49afdc978:3221125831a2f980139c34b35def3b0d',
        'logo': 'https://assets.livednow.com/logo/MytvSuper.png'
    },
    'EVT5': {
        'name': 'myTV SUPER 直播足球5台',
        'license': '54700d7a381b80ae395a312e03a9abeb:7c68d289628867bf691b42e90a50d349',
        'logo': 'https://assets.livednow.com/logo/MytvSuper.png'
    },
    'EVT6': {
        'name': 'myTV SUPER 直播足球6台',
        'license': 'e069fc056280e4caa7d0ffb99024c05a:d3693103f232f28b4781bbc7e499c43a',
        'logo': 'https://assets.livednow.com/logo/MytvSuper.png'
    },
        'C3': {
        'name': '互動窗 1',
        'license': 'f07372db27b162d69adf9aa612ae3364:da1631a2b2a836c5b7a3d044a18a4f16',
        'logo': 'https://assets.livednow.com/logo/MytvSuper.png'
    },
    'C2': {
        'name': '互動窗 2',
        'license': '1ba88eacde780c7567255b8b33026ae5:f7df792aab8992b79d72a8d01987ecb5',
        'logo': 'https://assets.livednow.com/logo/MytvSuper.png'
    }
}

def get_mytvsuper(channel):
    if channel not in CHANNEL_LIST:
        return '频道代号错误'

    api_token = os.getenv('MYTVSUPER_API_TOKEN')
    if not api_token:
        return 'API token 未设置'

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
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f'请求失败: {e}'

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
    m3u_file.write("#EXTM3U url-tvg=\"https://mytvsuperepg.860775.xyz/epg.xml\"\n")

    # 遍历所有频道并写入每个频道的 M3U 内容
    for channel_code in CHANNEL_LIST.keys():
        m3u_content = get_mytvsuper(channel_code)
        m3u_file.write(m3u_content)

print("所有频道的 M3U 播放列表已生成并保存为 'mytvsuper.m3u'。")
