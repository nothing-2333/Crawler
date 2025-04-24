from urllib.parse import quote, unquote
import curl_cffi.requests as requests
from typing import Optional, Dict, Union

from loguru import logger

class Request:
    def __init__(self, base_headers, proxies=None):
        if 'user-agent' not in base_headers:
            raise ValueError("基础请求头中需要包含符合规范的 'user-agent' 字段")
        
        # 获取 tls 指纹...

        self.base_headers = base_headers.copy()
        self.proxies = proxies.copy() if proxies else {}
        
        # cookies 中存入已经 url 编码过的值
        self._cookies = {}
    
    def delete_cookie(self, key):
        if key in self._cookies:
            del self._cookies[key]

    def get_cookie(self, key, is_decode=True):
        result = self._cookies[key]

        if is_decode:
            return unquote(result)
        return result
    
    def set_cookie(self, key, value, is_encode=True):
        if not isinstance(value, str) and value is not None:
            raise TypeError("cookie 的 value 值必须是 str 类型 或者 None。")
        
        if is_encode:
            key = quote(key)
            if value != None:
                value = quote(value)
        self._cookies[key] = value

    def _get_cookies_dict(self):
        cookies = self._cookies
        if not cookies:
            return {}

        return self._cookies

    def _get_cookies_str(self, cookies=None):
        if cookies == None:
            cookies = self._cookies
            
        if not cookies:
            return ""
        
        cookie_parts = []
        for k, v in cookies.items():
            if v != None:
                cookie_parts.append(f"{k}={v}")
            else:
                cookie_parts.append(k)
        
        return "; ".join(cookie_parts)
    
    def get_cookies(self, mode):
        if mode == 'dict':
            return self._get_cookies_dict()
        elif mode == 'str':
            return self._get_cookies_str()
        else:
            return None

    def _prepare_headers(self, custom_headers: Optional[Dict], cookies: Optional[Dict] = None) -> Dict:
        """合并基础头与自定义头（自定义头优先级更高）"""
        headers = self.base_headers.copy()
        if custom_headers:
            headers.update(custom_headers)
        # 添加编码后的 cookie 到头（需符合 HTTP 协议规范）
        cookies_str = self._get_cookies_str(cookies)
        if cookies_str:
            headers["cookie"] = cookies_str
        return headers

    def _request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict] = None,
        cookies: Optional[Dict] = None,
        **kwargs
    ) -> requests.Response:
        """统一请求方法"""
        merged_headers = self._prepare_headers(headers, cookies)

        try:
            # 发送请求
            response = requests.request(
                method,
                url,
                headers=merged_headers,
                proxies=self.proxies,
                impersonate="chrome110", # 这里先不添加 获取 tls 指纹...
                **kwargs
            )
            # 自动更新服务端返回的 cookie
            for name, value in response.cookies.items():
                print(value)
                logger.info(f"服务器设置 cookie: {name} -> {value}")
                self.set_cookie(name, value, False)
            return response
        except requests.RequestsError as e:
            raise RuntimeError(f"请求失败: {str(e)}") from e

    def get(self, url: str, **kwargs) -> requests.Response:
        """发送 GET 请求"""
        return self._request("GET", url, **kwargs)

    def post(self, url: str, **kwargs) -> requests.Response:
        """发送 POST 请求"""
        return self._request("POST", url, **kwargs)
# 示例使用
if __name__ == "__main__":

    pass