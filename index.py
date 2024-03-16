import sys
from pathlib import Path

import yaml

DIR = Path(__file__).resolve().parent

CONFIG_FILE = DIR / 'config.yaml'

with open(CONFIG_FILE, 'r') as f:
    CONFIG = yaml.safe_load(f)

DOMAIN = sys.argv[1]

CERT_FULLCHAIN = CERT_KEY = None
with open(f'{CONFIG["ssl_path"]}/{DOMAIN}/{CONFIG["cert_file_name"]}',
          'r') as f:
    CERT_FULLCHAIN = f.read()
with open(f'{CONFIG["ssl_path"]}/{DOMAIN}/{CONFIG["key_file_name"]}',
          'r') as f:
    CERT_KEY = f.read()

if __name__ == '__main__':
    if CONFIG['aliyun']['enabled']:
        import aliyun
        aliyun.main()

    # if CONFIG['dogecloud']['enabled']:
    #     import dogecloud
    #     dogecloud.main()

    # if CONFIG['tencent']['enabled']:
    #     import tencent
    #     tencent.main()
