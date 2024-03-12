import requests
import json

CHANNEL_LIST = {
'CWIN': {
        'name': 'SUPER FREE',
        'license': '0737b75ee8906c00bb7bb8f666da72a0:15f515458cdb5107452f943a111cbe89'
    },
'C18': {
        'name': 'myTV SUPER 18台',
        'license': '72de7d0a1850c8d40c5bdf9747a4ca7c:4967537ff0bc8209277160759de4adef'
    },
'TVG': {
        'name': '黃金翡翠台',
        'license': '8fe3db1a24969694ae3447f26473eb9f:5cce95833568b9e322f17c61387b306f'
    },
'JUHD': {
        'name': '翡翠台(超高清)',
        'license': '2c045f5adb26d391cc41cd01f00416fa:fc146771a9b096fc4cb57ffe769861be'
    },
'J': {
        'name': '翡翠台',
        'license': '0958b9c657622c465a6205eb2252b8ed:2d2fd7b1661b1e28de38268872b48480'
    },
'B': {
        'name': 'J2',
        'license': '56603b65fa1d7383b6ef0e73b9ae69fa:5d9d8e957d2e45d8189a56fe8665aaaa'
    },
'C': {
        'name': '無綫新聞台',
        'license': '90a0bd01d9f6cbb39839cd9b68fc26bc:51546d1f2af0547f0e961995b60a32a1'
    },
'P': {
        'name': '明珠台',
        'license': 'e04facdd91354deee318c674993b74c1:8f97a629de680af93a652c3102b65898'
    },
'A': {
        'name': '無綫財經 體育 資訊台',
        'license': '91db728a2806d0a0bbb9d92e608f5498:6e96ea66f51b2b9c16c5d6c5b3314a86'
    },
'CTVC': {
        'name': '千禧經典台',
        'license': '6c308490b3198b62a988917253653692:660578b8966fe8012ad51b9aae7a5d78'
    },
'CTVS': {
        'name': '亞洲劇台',
        'license': 'df5c0e617dffc3e3c44cb733dccb33c0:7d00ec9cd4f54d5baf94c03edc8cfe25'
    },
'CDR3': {
        'name': '華語劇台',
        'license': 'baae227b5fc06e2545868d4a1c9ced14:8cd460458b0bdecca5c12791b6409278'
    },
'TVO': {
        'name': '黃金華劇台',
        'license': 'acd93a5f665efd4feadb26f5ed48fd96:c6ce58ef9cce30638e0c2e9fc45a6dbd'
    },
'CTVE': {
        'name': '娛樂新聞台',
        'license': '6fa0e47750b5e2fb6adf9b9a0ac431a3:a256220e6c2beaa82f4ca5fba4ec1f95'
    },
'CCOC': {
        'name': '戲曲台',
        'license': 'c91c296ef6c46b3f2af1da257553bd17:d6e92d5e594f6f8e494a6e1c9df75298'
    },
'KID': {
        'name': 'SUPER Kids Channel',
        'license': '42527ca90ad525ba2eac9979c93d3bca:b730006ad1da48b412ceb1f9e36a833d'
    },
'ZOO': {
        'name': 'ZooMoo',
        'license': '9c302eb50bef5a9589d97cb90982b05e:2603e646caafe22bc4e8a17b5a2dd55b'
    },
'CNIKO': {
        'name': 'Nickelodeon',
        'license': '0e69430290ed7b00af4db78419dcad8b:e4769b57a66e8e9737d6d86f317600c0'
    },
'CNIJR': {
        'name': 'Nick Jr',
        'license': '9f1385d2a12a67b572b9d968eb850337:3086bcd49a909606a8686858c05c7e33'
    },
'CCLM': {
        'name': '粵語片台',
        'license': '5b90da7fd2f018bf85a757241075626f:75c0897b4cf5ce154ddae86eddb79cd3'
    },
'CMAM': {
        'name': '美亞電影台',
        'license': 'c5d6f2afbd6b276312b0471a653828e1:ecbbb4a3ffa2200ae69058e20e71e91b'
    },
'CTHR': {
        'name': 'Thrill',
        'license': 'b22355363ab2b09a6def54be0c89b9f2:4b196c2bf24b37e82a81031246de6efe'
    },
'CCCM': {
        'name': '天映經典頻道',
        'license': '627b6ca150887912bec47ae4a9b85269:2bf49b2105d20544a6db89c0577b9802'
    },
'CMC': {
        'name': '中國電影頻道',
        'license': 'cabb16d20e71b512f24e9ece0cb09396:2d43505980a22014ee1a476880982308'
    },
'CRTX': {
        'name': 'ROCK Action',
        'license': '358eacad1f06e8e375493dabee96d865:461a02b2eb1232c6c100b95bd0bf40f8'
    },
'CKIX': {
        'name': 'KIX',
        'license': '3b4a44c5ef3217c55a357ad976d328b2:f3355e5a30722e631031b851642c27f1'
    },
'LNH': {
        'name': 'Love Nature HD',
        'license': '03fb0f439f942f50d06bf23a511bf4f8:bae7115da07195263e50ae5fc8bbe4f3'
    },
'LN4': {
        'name': 'Love Nature 4K',
        'license': '037c644cb92137ac5c8d653e952e4c8f:b3b2fcbe576a63cf3bbb9425da3de4cf'
    },
'SMS': {
        'name': 'Global Trekker',
        'license': 'a8f381c2a3114cc6c55f50b6ff0c78f3:86922e5993788488e1eca857c00d4fab'
    },
'CRTE': {
        'name': 'ROCK綜藝娛樂',
        'license': '002d034731b6ac938ea7ba85bc3dc759:6694258c023d73492a10acb860bc6161'
    },
'CAXN': {
        'name': 'AXN',
        'license': '20bea0e14af0d3dcb63d4126e8b50172:07382de357a2b0cceabe82e0b37cb8de'
    },
'GEM': {
        'name': 'GEM',
        'license': '5ff464c783f3a30b3cacab585a3ed42f:2325cbea6cd3ebe9c09d733426bfde7c'
    },
'CANI': {
        'name': 'Animax',
        'license': 'b1a073dbd8272b0c99940db624ce8d74:9fec26ff4c6774a8bde881e5cb0fe82e'
    },
'CJTV': {
        'name': 'tvN',
        'license': 'adcab9e8e5644ff35f04e4035cc6ad3b:d8e879e108a96fde6537c1b679c369b5'
    },
'CTS1': {
        'name': '無線衛星亞洲台',
        'license': 'ad7b06658e8a36a06def6b3550bde35c:b672f89570a630abb1d2abb5030e6303'
    },
'CRE': {
        'name': '創世電視',
        'license': 'adef00c5ba927d01642b1e6f3cedc9fb:b45d912fec43b5bbd418ea7ea1fbcb60'
    },
'FBX': {
        'name': 'FashionBox',
        'license': '4df52671ef55d2a7ac03db75e9bba2f7:4a3c16e8098c5021f32c7d4f66122477'
    },
'CMEZ': {
        'name': 'Mezzo Live HD',
        'license': 'e46f2747a9cf6822a608786bbc21d400:d8778fcf92c949e949a6700828f5f67e'
    },
'DTV': {
        'name': '東方衛視國際頻道',
        'license': '9d6a139158dd1fcd807d1cfc8667e965:f643ba9204ebba7a5ffd3970cfbc794c'
    },
'PCC': {
        'name': '鳳凰衛視中文台',
        'license': '7bca0771ba9205edb5d467ce2fdf0162:eb19c7e3cea34dc90645e33f983b15ab'
    },
'PIN': {
        'name': '鳳凰衛視資訊台',
        'license': '83f7d313adfc0a5b978b9efa0421ce25:ecdc8065a46287bfb58e9f765e4eec2b'
    },
'PHK': {
        'name': '鳳凰衛視香港台',
        'license': 'cde62e1056eb3615dab7a3efd83f5eb4:b8685fbecf772e64154630829cf330a3'
    },
'CMN1': {
        'name': '神州新聞台',
        'license': '7ee6ed08925f4716c8d0943e7bdb3e5f:6f3c1e31b30ccac36d466f41489ceb27'
    },
'CTSN': {
        'name': '無線衛星新聞台',
        'license': '73aaeb9e84db423627018017059e0f9d:34148a56250459383f7ef7369073bf39'
    },
'CCNA': {
        'name': '亞洲新聞台',
        'license': 'ddc7bb2603628134334919a0d7327d1d:a5fcd8bb852371faedd13b684f5adede'
    },
'CJAZ': {
        'name': '半島電視台英語頻道',
        'license': '80c76105d3ae35dfe25f939d1fb83383:6d76e7ba039773bced47d78e6de4fcf0'
    },
'CF24': {
        'name': 'France 24',
        'license': '2d4f6b8755a918d2126a2ee78791cf0b:c392acc1a1a070d2bcdf518d99d88406'
    },
'CDW1': {
        'name': 'DW',
        'license': '2bb557c09dfc01a27ab81778913f2a10:d00ca6eb9a83ffde846324109fb445ba'
    },
'CNHK': {
        'name': 'NHK World-Japan',
        'license': '9c2ecde1c31185ab61ed4689b87ae332:54895a656e053a73b39882e7a56d642b'
    },
'CARI': {
        'name': 'Arirang TV',
        'license': 'f3ae14e72f585eaf14b18d8d9515d43f:ce0e375c3966263877078aadd815742e'
    },
'EVT1': {
        'name': 'myTV SUPER直播足球1台',
        'license': 'e8ca7903e25450d85cb32b3057948522:d5db5c03608f5f6c8a382c6abcb829e4'
    },
'EVT2': {
        'name': 'myTV SUPER直播足球2台',
        'license': '024f2733fb9afad23490149c601ce47c:034db34d56263c79c7f41448f2a6cfc1'
    },
'EVT3': {
        'name': 'myTV SUPER直播足球3台',
        'license': '84f456002b780253dab5534e9713323c:65aeb769264f41037cec607813e91bae'
    },
'EVT4': {
        'name': 'myTV SUPER直播足球4台',
        'license': '848d6d82c14ffd12adf4a7b49afdc978:3221125831a2f980139c34b35def3b0d'
    },
'EVT5': {
        'name': 'myTV SUPER直播足球5台',
        'license': '54700d7a381b80ae395a312e03a9abeb:7c68d289628867bf691b42e90a50d349'
    },
}


def get_mytvsuper(channel: str):
    if channel not in CHANNEL_LIST:
        print('频道代号错误')
        return

    api_token = ''  # 请自行获取
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {api_token}',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Host': 'user-api.mytvsuper.com',
        'Origin': 'https://www.mytvsuper.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.2 Safari/605.1.15',
        'Referer': 'https://www.mytvsuper.com/',
        'X-Forwarded-For': '210.6.4.148',  # 香港原生IP
    }

    params = {
        'platform': 'android_tv',
        'network_code': channel,
    }

    response = requests.get(url='https://user-api.mytvsuper.com/v1/channel/checkout',
                            params=params, headers=headers)
    if response.status_code != 200:
        print('请求失败')

    response_json = response.json()
    profiles = response_json.get('profiles', [])
    play_url = ''
    for i in profiles:
        if i['quality'] == 'high':
            play_url = i['streaming_path']
            break

    if not play_url:
        print('未找到播放地址')
    play_url = play_url.split('&p=')[0]
    print('-------')
    print('URL:', play_url)
    print('-------')
    print('License:', CHANNEL_LIST[channel]['license'])
    print('-------')
    license_dict = {s[0]: s[1] for s in [i.split(':') for i in CHANNEL_LIST[channel]['license'].split(';')]}
    print('License Json:', json.dumps(license_dict))
    print('-------')


if __name__ == '__main__':
    print('---- mytvsuper ----')
    for channel in CHANNEL_LIST:
        print(f'[{channel}] {CHANNEL_LIST[channel]["name"]}')
    
    channel = input('\n请输入频道代号:')
    get_mytvsuper(channel)
