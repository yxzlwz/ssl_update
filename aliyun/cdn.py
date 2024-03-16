from index import DOMAIN, CERT_FULLCHAIN, CERT_KEY
from aliyun import client

import json

from aliyunsdkcdn.request.v20180510.BatchSetCdnDomainServerCertificateRequest import BatchSetCdnDomainServerCertificateRequest
from aliyunsdkcdn.request.v20180510.DescribeUserDomainsRequest import DescribeUserDomainsRequest


def upadte_domains(cert_name):
    request = DescribeUserDomainsRequest()
    request.set_accept_format('json')
    request.set_PageSize(50)
    request.set_DomainSearchType("suf_match")
    request.set_DomainName(DOMAIN)
    response = client.do_action_with_exception(request)
    certs = json.loads(str(response, encoding='utf-8'))['Domains']['PageData']
    print('域名搜索结果', certs)

    domains = []
    for i in certs:
        if i['DomainName'].endswith(DOMAIN) and i['DomainName'].count(
                '.') <= DOMAIN.count('.') + 1:
            domains.append(i['DomainName'])

    while len(domains) > 0:
        _domains = domains[:10]
        request = BatchSetCdnDomainServerCertificateRequest()
        request.set_DomainName(','.join(_domains))
        request.set_accept_format('json')
        request.set_CertName(cert_name)
        request.set_CertType("upload")
        request.set_SSLProtocol("on")
        request.set_SSLPub(CERT_FULLCHAIN)
        request.set_SSLPri(CERT_KEY)
        request.set_ForceSet("1")
        response = client.do_action_with_exception(request)

        domains = domains[10:]


def main(cert_name):
    upadte_domains(cert_name)
