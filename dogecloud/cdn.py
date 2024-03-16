from index import DOMAIN

from dogecloud import dogecloud_api


def update(domain_id, cert_id):
    print(
        f'更新域名id={domain_id}使用的SSL证书',
        dogecloud_api(
            f'/cdn/domain/config.json?id={domain_id}',
            {'cert_id': cert_id},
        ),
    )


def main(cert_id):
    response = dogecloud_api('/cdn/domain/list.json')
    print('域名搜索结果', response['data']['domains'])
    for i in response['data']['domains']:
        if i['name'].endswith(DOMAIN) and i['name'].count(
                '.') <= DOMAIN.count('.') + 1:
            update(i['id'], cert_id)


if __name__ == '__main__':
    main()
