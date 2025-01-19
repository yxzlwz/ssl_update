# SSL Update

## 简介

目前，自动申请和管理免费SSL证书的项目有很多，如个人正在使用的 [acme.sh](https://github.com/acmesh-official/acme.sh)。然而在申请后，如果我们的需求不仅限于服务器本地的使用，证书的部署也是一件麻烦事。

本项目旨在解决这个问题：这是一个将证书上传到各个云服务商主流产品的脚本集合，且在很大程度上支持大家根据个人需求进行配置。

为了不重复造轮子，我们没有实现证书申请功能。我们更建议您将此项目作为 acme.sh 的补充，具体将在下文中介绍。

考虑到目前主要适配的是国内的云服务商，暂不提供英文文档。

## 适配情况

目前已适配的云服务商产品有：

- [x] 阿里云
  - [x] CDN
  - [x] DCDN
  - [x] 视频直播
- [x] 腾讯云
  - [x] CDN
  - [x] API 网关
- [x] DogeCloud
  - [x] CDN

## 目录结构

默认情况下，你需要在项目根目录下创建 `ssl` 文件夹，对于每个域名，在该文件夹中创建以证书签发域名为名的文件夹，其内存放公钥文件 `cert.pem` 和私钥文件 `key.pem`。

如我的域名是 `yixiangzhilv.com`，那么目录结构应如下：

```
ssl
└── yixiangzhilv.com
    ├── cert.pem
    └── key.pem
```

目录和文件名可以在配置文件中进行修改。

特别说明的是，目前进行测试时使用的域名都是 ZeroSSL 签发的通配符域名。例如你的域名是 `yixiangzhilv.com`，那么对应的证书应同时签发给 `yixiangzhilv.com` 和 `*.yixiangzhilv.com`。

## 配置文件

复制 `config.example.yaml` 为 `config.yaml`，并根据个人需求进行修改。

对于不需要的云服务商，可以将其对应的 `enabled` 字段设为 `false`；对于不需要的产品，可以为其对应的 `enabled_products` 字段添加注释。

对于部分必须按地域获取业务列表的服务（如腾讯云API网关），为了性能考虑，你需要手动指定你拥有业务的地域。

请确保正确配置各个云服务商的 API 密钥，且为配置的密钥赋予了足够的权限。除了你需要的产品的管理权限外，对于部分云服务商（如腾讯云），本项目还需要操作 SSL 证书的权限。

## 使用方法

在配置好 `config.yaml` 后，运行命令如下：

```bash
python3 index.py yixiangzhilv.com
```

其中`yixiangzhilv.com`是你的域名，**该参数必须添加**。

要想在后续 acme.sh 自动更新域名证书时推送证书也自动生效的话，运行一次如下命令：

```bash
acme.sh --force --renew -d example.com --renew-hook "python3 /path/to/index.py example.com"
```

这样，就会立即强制更新证书并推送到云服务商，并且下次自动更新时也有效。
