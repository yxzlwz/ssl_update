from index import CERT_FULLCHAIN, CERT_KEY, DOMAIN, CONFIG

import hmac
import json
import random
import urllib
from hashlib import sha1

import requests

config = CONFIG['dogecloud']
ACCESS_KEY = config['access_key']
ACCESS_TOKEN = config['access_token']


def dogecloud_api(api_path, data={}, post=True, json_mode=True):
    body = ''
    mime = ''
    if post:
        if json_mode:
            body = json.dumps(data)
            mime = 'application/json'
        else:
            body = urllib.parse.urlencode(data)
            mime = 'application/x-www-form-urlencoded'
    sign_str = api_path + "\n" + body
    signed_data = hmac.new(ACCESS_TOKEN.encode('utf-8'),
                           sign_str.encode('utf-8'), sha1)
    sign = signed_data.digest().hex()
    authorization = 'TOKEN ' + ACCESS_KEY + ':' + sign
    if post:
        response = requests.post('https://api.dogecloud.com' + api_path,
                                 data=body,
                                 headers={
                                     'Authorization': authorization,
                                     'Content-Type': mime
                                 })
    else:
        response = requests.post('https://api.dogecloud.com' + api_path,
                                 headers={
                                     'Authorization': authorization,
                                 })
    return response.json()


def search_domains():
    response = dogecloud_api('/cdn/domain/list.json')
    print('域名搜索结果', response['data']['domains'])
    for i in response['data']['domains']:
        if i['name'].endswith(DOMAIN) and i['name'].count(
                '.') <= DOMAIN.count('.') + 1:
            print(i, '(跳过)')
            continue
            update(i['id'])


def upload():
    response = dogecloud_api('/cdn/cert/upload.json', {
        'note': str(random.randint(100000, 999999)),
        'cert': CERT_FULLCHAIN,
        'private': CERT_KEY
    },
                             json_mode=False)
    cert_id = str(response['data']['id'])
    print('证书上传结果', response)
    return cert_id


def main():
    cert_id = upload()

    if 'cdn' in config['enabled_products']:
        import dogecloud.cdn as cdn
        cdn.main(cert_id)


if __name__ == '__main__':
    main()
