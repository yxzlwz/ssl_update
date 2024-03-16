from index import DOMAIN, CERT_FULLCHAIN, CERT_KEY

import json

from aliyunsdklive.request.v20161101.DescribeLiveUserDomainsRequest import \
    DescribeLiveUserDomainsRequest
from aliyunsdklive.request.v20161101.SetLiveDomainCertificateRequest import \
    SetLiveDomainCertificateRequest
from aliyun import client


def update(domain, cert_name):
    request = SetLiveDomainCertificateRequest()
    request.set_accept_format('json')

    request.set_DomainName(domain)
    request.set_SSLProtocol("on")
    request.set_CertName(cert_name)
    request.set_CertType("upload")
    request.set_SSLPub(CERT_FULLCHAIN)
    request.set_SSLPri(CERT_KEY)
    request.set_ForceSet("1")
    response = client.do_action_with_exception(request)
    print(f'更新域名{domain}使用的SSL证书', str(response, encoding='utf-8'))


def search_domains(cert_name):
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
        update(i['DomainName'], cert_name)


def main(cert_name):
    search_domains(cert_name)
