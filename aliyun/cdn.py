from index import DOMAIN, CERT_FULLCHAIN, CERT_KEY
from aliyun import client

import json

from aliyunsdkcdn.request.v20180510.BatchSetCdnDomainServerCertificateRequest import BatchSetCdnDomainServerCertificateRequest
from aliyunsdkdcdn.request.v20180115.BatchSetDcdnDomainCertificateRequest import BatchSetDcdnDomainCertificateRequest
from aliyunsdkcdn.request.v20180510.DescribeUserDomainsRequest import DescribeUserDomainsRequest
from aliyunsdkdcdn.request.v20180115.DescribeDcdnUserDomainsRequest import DescribeDcdnUserDomainsRequest


def upadte_domains(cert_name, uploaded):
    request = DescribeUserDomainsRequest()
    request.set_accept_format('json')
    request.set_PageSize(50)
    request.set_DomainSearchType("suf_match")
    request.set_DomainName(DOMAIN)
    response = client.do_action_with_exception(request)
    certs = json.loads(str(response, encoding='utf-8'))['Domains']['PageData']
    print('CDN域名搜索结果', certs)

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
        request.set_SSLProtocol("on")
        request.set_ForceSet("1")
        if uploaded:
            request.set_CertType("cas")
        else:
            request.set_CertType("upload")
            request.set_SSLPub(CERT_FULLCHAIN)
            request.set_SSLPri(CERT_KEY)
            uploaded = True
        response = client.do_action_with_exception(request)

        domains = domains[10:]

    request = DescribeDcdnUserDomainsRequest()
    request.set_accept_format('json')
    request.set_PageSize(50)
    request.set_DomainSearchType("suf_match")
    request.set_DomainName(DOMAIN)
    response = client.do_action_with_exception(request)
    response_dict = json.loads(str(response, encoding='utf-8'))
    certs = response_dict['Domains']['PageData']
    print('DCDN域名搜索结果', certs)

    domains = []
    for i in certs:
        if i['DomainName'].endswith(DOMAIN) and i['DomainName'].count(
                '.') <= DOMAIN.count('.') + 1:
            domains.append(i['DomainName'])

    while len(domains) > 0:
        _domains = domains[:10]
        request = BatchSetDcdnDomainCertificateRequest()
        request.set_DomainName(','.join(_domains))
        request.set_accept_format('json')
        request.set_CertName(cert_name)
        request.set_SSLProtocol("on")
        if uploaded:
            request.set_CertType("cas")
        else:
            request.set_CertType("upload")
            request.set_SSLPub(CERT_FULLCHAIN)
            request.set_SSLPri(CERT_KEY)
            uploaded = True
        response = client.do_action_with_exception(request)

        domains = domains[10:]

    return uploaded


def main(cert_name, uploaded):
    uploaded = upadte_domains(cert_name, uploaded)
    return uploaded
