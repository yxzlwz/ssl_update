from index import CERT_FULLCHAIN, CERT_KEY, DOMAIN, CONFIG
from utils import random_str

from tencentcloud.common import credential
from tencentcloud.ssl.v20191205 import ssl_client, models

config = CONFIG['tencent']
TENCENT_SECRET_ID = config.get("secret_id")
TENCENT_SECRET_KEY = config.get("secret_key")

cred = credential.Credential(TENCENT_SECRET_ID, TENCENT_SECRET_KEY)


def upload_certificate():
    client = ssl_client.SslClient(cred, '')

    request = models.UploadCertificateRequest()
    request.Alias = f"{DOMAIN}_{random_str(4)}"
    request.CertificateType = "SVR"
    request.CertificatePublicKey = CERT_FULLCHAIN
    request.CertificatePrivateKey = CERT_KEY
    response = client.UploadCertificate(request)

    return response.CertificateId


def main():
    certificate_id = upload_certificate()

    if 'apigateway' in config['enabled_products']:
        import tencent.apigateway as apigateway
        apigateway.main(certificate_id)

    if 'cdn' in config['enabled_products']:
        import tencent.cdn as cdn
        cdn.main(certificate_id)


if __name__ == '__main__':
    main()
