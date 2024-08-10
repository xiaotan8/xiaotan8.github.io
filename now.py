import requests
import re
import ssl

# Create a custom SSL context that ignores the DH key size error
class SSLAdapter(requests.adapters.HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.set_ciphers('DEFAULT@SECLEVEL=1')
        super().__init__(*args, **kwargs)
    
    def send(self, request, **kwargs):
        kwargs['timeout'] = (10, 30)  # Adjust timeouts if needed
        return super().send(request, **kwargs)

# Define the URL and headers
url = 'https://webtvapi.now.com/10/7/getLiveURL'
headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'NNC/6.3.0 (com.now.news; build:2309121224; iOS 17.1.0) Alamofire/5.2.2'
}

# Define the body
body = {
    'deviceType': 'IOS_PHONE',
    'contentId': '332',
    'audioCode': 'A',
    'deviceId': '8269809F-7702-45CE-9378-D7157A2E6819',
    'mode': 'prod',
    'callerReferenceNo': '20140702122500',
    'contentType': 'Channel'
}

# Make the POST request with custom SSL context
session = requests.Session()
session.mount('https://', SSLAdapter())
response = session.post(url, headers=headers, json=body)
response.raise_for_status()  # Raise an error for bad responses

# Parse the JSON response
response_data = response.json()
asset_url = response_data['asset'][0]

# Fetch the M3U8 content
m3u8_response = session.get(asset_url)
m3u8_response.raise_for_status()
m3u8_content = m3u8_response.text

# Determine the base URL
base_url = re.sub(r'/07\.m3u8.*', '', asset_url) + '/'

# Generate the play URL
play_url = re.sub(r'(.*?).ts', base_url + r'\1.ts', m3u8_content)

# Save the play URL to a file
with open('now.m3u8', 'w') as file:
    file.write(play_url)
