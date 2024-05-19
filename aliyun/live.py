from index import DOMAIN, CERT_FULLCHAIN, CERT_KEY

import json

from aliyunsdklive.request.v20161101.DescribeLiveUserDomainsRequest import \
    DescribeLiveUserDomainsRequest
from aliyunsdklive.request.v20161101.SetLiveDomainCertificateRequest import \
    SetLiveDomainCertificateRequest
from aliyun import client


def update(domain, cert_name, uploaded):
    request = SetLiveDomainCertificateRequest()
    request.set_accept_format('json')

    request.set_DomainName(domain)
    request.set_SSLProtocol("on")
    request.set_CertName(cert_name)
    request.set_ForceSet("1")
    if uploaded:
        request.set_CertType("cas")
    else:
        request.set_CertType("upload")
        request.set_SSLPub(CERT_FULLCHAIN)
        request.set_SSLPri(CERT_KEY)
        uploaded = True
    response = client.do_action_with_exception(request)
    print(f'更新域名{domain}使用的SSL证书', str(response, encoding='utf-8'))
    return uploaded


def search_domains(cert_name, uploaded):
    request = DescribeLiveUserDomainsRequest()
    request.set_accept_format('json')
    request.set_PageSize(50)
    request.set_DomainSearchType('suf_match')
    request.set_DomainName(DOMAIN)
    response = client.do_action_with_exception(request)
    domains = json.loads(str(response,
                             encoding='utf-8'))['Domains']['PageData']
    print('域名搜索结果', domains)
    for i in domains:
        uploaded = update(i['DomainName'], cert_name, uploaded)

    return uploaded


def main(cert_name, uploaded):
    uploaded = search_domains(cert_name, uploaded)
    return uploaded
