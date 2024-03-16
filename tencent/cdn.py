from index import DOMAIN

from tencent import cred

import json

from tencentcloud.cdn.v20180606 import cdn_client, models


def update(domain, certificate_id):
    try:
        client = cdn_client.CdnClient(cred, "")

        req = models.UpdateDomainConfigRequest()
        params = {
            "Domain": domain,
            "Https": {
                "Switch": "on",
                "CertInfo": {
                    "CertId": certificate_id
                }
            }
        }
        req.from_json_string(json.dumps(params))
        resp = client.UpdateDomainConfig(req)
        print(f'{domain}更新成功', resp.to_json_string())

    except Exception as err:
        print(err)


def search_domains(certificate_id):
    try:
        client = cdn_client.CdnClient(cred, "")

        req = models.DescribeDomainsRequest()
        params = {
            "Limit": 1000,
            "Filters": [{
                "Name": "domain",
                "Value": [DOMAIN],
                "Fuzzy": True
            }]
        }
        req.from_json_string(json.dumps(params))

        resp = client.DescribeDomains(req)
        data = resp._serialize()['Domains']
        print(data)
        for i in data:
            update(i['Domain'], certificate_id)

    except Exception as err:
        print(err)


def main(certificate_id):
    search_domains(certificate_id)


if __name__ == '__main__':
    main()
