# Crawler

## 一个低耦合的爬虫框架，由 python 实现了请求逻辑，逻辑更清晰，利用 socket 实现 rpc 以调用其他语言实现加密逻辑，低耦合方便的添加更多可供调用的语言。

在使用 Request 模块处理 cookie 时，你必须时刻注意 cookie 是否需要 url 编码或解码

## 小贴士
`JSON.stringify(data) == json.dumps(data, ensure_ascii=False, separators=(',', ':'))`