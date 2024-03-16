from index import DOMAIN, CONFIG, CERT_FULLCHAIN, CERT_KEY

config = CONFIG['aliyun']

ACCESS_KEY = config.get('access_key')
ACCESS_TOKEN = config.get('access_token')

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.auth.credentials import AccessKeyCredential
from aliyunsdkcas.request.v20180713.CreateUserCertificateRequest import CreateUserCertificateRequest
from utils import random_str

client = AcsClient(credential=AccessKeyCredential(ACCESS_KEY, ACCESS_TOKEN))


# 由于阿里云的限制，我们暂时停用这一接口，具体情况请见 README.md
# def upload(cert_name):
#     request = CreateUserCertificateRequest()
#     request.set_Name(cert_name)
#     request.set_Cert(CERT_FULLCHAIN)
#     request.set_Key(CERT_KEY)
#     response = client.do_action_with_exception(request)
#     print('证书上传成功', response)


def main():
    cert_name = f'{DOMAIN}_{random_str(4)}'
    # upload(cert_name)

    if 'cdn' in config['enabled_products']:
        import aliyun.cdn as cdn
        cdn.main(cert_name)

    if 'live' in config['enabled_products']:
        import aliyun.live as live
        live.main(cert_name)
