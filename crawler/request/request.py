from urllib.parse import urlparse, quote, unquote
from collections import defaultdict

class Request:
    def __init__(self, init_headers=None):
        # 初始化请求头，其他请求会在这个基础上自定义
        if init_headers == None:
            self.init_headers = {}
        else:
            if isinstance(init_headers, dict):
                self.init_headers = init_headers
            else:
                raise TypeError("init_headers 应该传入一个 dict")
        # 管理 cookie 不会自动 url 编码
        self.cookies = defaultdict(dict)            # self.cookies['example.com']['key'] = 'value'
    
    def update_cookies(self, host, cookies):
        if not isinstance(cookies, dict):
            raise TypeError("传入的 cookies 必须是一个 dict。")
        
        for k, v in cookies.items():
            if not isinstance(v, str):
                raise TypeError("cookie 的 value 值必须是 str 类型。")
            self.cookies[host][k] = v
            
    def delete_cookie(self, host, key):
        del self.cookies[host][key]
        
    def update_init_headers(self, headers):
        if not isinstance(headers, dict):
            raise TypeError("传入的 headers 必须是一个 dict。")
        
        self.init_headers.update(headers)

    def get_cookie_str(self, host, is_url_encode=True):
        cookies = self.cookies.get(host, {})
        if not cookies:
            return ""
        
        # 处理编码逻辑
        cookie_parts = []
        for k, v in cookies.items():
            if not isinstance(v, str):
                raise TypeError("cookie 的 value 值必须是 str 类型。")

            if is_url_encode:
                v = quote(v)
                k = quote(k)
            cookie_parts.append(f"{k}={v}")
        
        # 规范分隔符格式
        return "; ".join(cookie_parts)

# 示例使用
if __name__ == "__main__":

    pass