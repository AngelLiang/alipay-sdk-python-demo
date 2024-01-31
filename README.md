# 支付宝python sdk使用示例

## 测试环境

- windows 10
- python 310
- poetry

## 快速开始

安装环境

```
poetry install
```

进入支付宝的sandbox环境，获取环境变量

https://open.alipay.com/develop/sandbox/app


配置环境变量

```
cp .env.example
```

- ALIPAY_SERVER_URL: 网关地址
- ALIPAY_APPID: 应用appid
- ALIPAY_APP_PRIVATE_KEY: 私钥
- ALIPAY_PUBLIC_KEY: 公钥
- BUYER_UID: 购买者支付宝的uid

