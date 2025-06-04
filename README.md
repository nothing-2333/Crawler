# Crawler

## 为什么要自己写一个爬虫框架（核心思想）
我试过用一些比较成熟的主流框架像 `Scrapy` `PySpider` 感觉搞得太复杂了, 各种管道、分布式、数据库...看的人头晕眼花, 我在做逆向、爬虫项目时, 我觉得只用做好三件事: 环境指纹、加密算法、请求接口, 剩下的就是将他们合理组合起立就大功告成, 而接下来是建立 web 后端服务还是存入数据库亦或者本地跑...就随你心意再自己加模块。

## 初步使用

### 环境指纹 `crawler/env`
要加密环境指纹值都放在 `crawler/env/fingerprints-store` 中, 提供了随机取一套或者根据文件名取一套的功能, 用 Env 类加载到内存中。

### 加密算法 `crawler/encrypt`
`crawler/encrypt/encrypt.py` 是对外统一接口, 负责调度已经写好的在其他文件中的算法。具体算法的实现被放在了`crawler/encrypt/impl`文件夹下。 并且还提供了 rpc 服务, 可以通过起一个子线程用本地的 socket 来与其他语言通信, 条用其他语言的算法, 在 `crawler/encrypt/rpc` 中 server-of-* 是已经支持的 rpc 语言, 随着我的使用会慢慢增加, 你也可以照着现有的格式自行添加新的语言, 欢迎 pr。而已经提供好的服务只需要在构建 `Encrypt` 类时输入一个 dict 配置就可以了。

### 请求接口 `crawler/crawler.py`
将请求的接口写在 Crawler 类中, 一个 url 是一个方法, Crawler 可以集成 Env 实例和 Encrypt 实例。

### 串联逻辑 `main.py`
在这个文件中只需要使用前面已经提供的服务, 将前后逻辑组合起来就可以了, 建立 web 服务、写入数据库、本地跑...

## 进阶使用

### 打包 Crawler 实例 `crawler/serializer.py`
提供两个工具函数可以将内存中的 Crawler 实例转换成字符串, 也可以直接从字符串加载出一个实例。

### 自定义的 request
封装了一个自己发包方法, 为了更简单的管理 cookies 并且处理 tls 检测。
- 管理 cookies: 我将所有 cookie 存到一起, 不管他们是哪个域名的, 用的时候可以直接传入一个包含需要的 cookie 名的 list, 同时也支持传入其他类型, dict、str。
- 处理 tls 检测: 计划是效仿 curl_cffi, 不直接用 curl_cffi 是因为不支持 ja4。

## 小贴士
`JSON.stringify(data) == json.dumps(data, ensure_ascii=False, separators=(',', ':'))`