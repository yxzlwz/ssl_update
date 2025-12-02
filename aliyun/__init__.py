from index import DOMAIN, CONFIG, CERT_FULLCHAIN, CERT_KEY

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.auth.credentials import AccessKeyCredential
from utils import random_str

config = CONFIG['aliyun']

ACCESS_KEY = config.get('access_key')
ACCESS_TOKEN = config.get('access_token')

client = AcsClient(credential=AccessKeyCredential(ACCESS_KEY, ACCESS_TOKEN))


def main():
    cert_name = f'{DOMAIN}_{random_str(4)}'
    uploaded = False

    if 'cdn' in config['enabled_products']:
        import aliyun.cdn as cdn

        uploaded = cdn.main(cert_name, uploaded)

    if 'live' in config['enabled_products']:
        import aliyun.live as live

        uploaded = live.main(cert_name, uploaded)
