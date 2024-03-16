from index import DOMAIN, CONFIG

from tencent import cred

import json

from tencentcloud.apigateway.v20180808 import apigateway_client, models

config = CONFIG['tencent']


def update(
    client: apigateway_client.ApigatewayClient,
    service_id,
    domain,
    certificate_id,
):
    try:
        req = models.ModifySubDomainRequest()
        params = {
            "ServiceId": service_id,
            "SubDomain": domain,
            "CertificateId": certificate_id,
            "IsDefaultMapping": True
        }
        req.from_json_string(json.dumps(params))
        resp = client.ModifySubDomain(req)
        print(f'{domain}更新成功', resp.to_json_string())

    except Exception as err:
        print(err)


def search_domains(
    client: apigateway_client.ApigatewayClient,
    service_id,
    certificate_id,
):
    try:
        req = models.DescribeServiceSubDomainsRequest()
        params = {
            "ServiceId": service_id,
            "Limit": 100,
        }
        req.from_json_string(json.dumps(params))

        resp = client.DescribeServiceSubDomains(req)
        data = resp._serialize()['Result']
        for i in data['DomainSet']:
            if i['DomainName'].endswith(DOMAIN):
                update(client, service_id, i['DomainName'], certificate_id)

    except Exception as err:
        print(err)


def search_services(
    client: apigateway_client.ApigatewayClient,
    certificate_id,
):
    try:
        req = models.DescribeServicesStatusRequest()
        req.from_json_string(json.dumps({"Limit": 100}))

        resp = client.DescribeServicesStatus(req)
        data = resp._serialize()['Result']

        for i in data['ServiceSet']:
            search_domains(client, i['ServiceId'], certificate_id)

    except Exception as err:
        print(err)


def main(certificate_id):
    for region in config['regions']:
        client = apigateway_client.ApigatewayClient(cred, region)
        search_services(client, certificate_id)
