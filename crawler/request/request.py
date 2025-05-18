
import curl_cffi.requests as requests
from urllib.parse import quote, unquote
from loguru import logger

from .cookies import Cookies
from .cookie_value import CookieValue

class Request:
    def __init__(self, base_headers, cookies=None, proxies=None, is_print=True):
        if 'user-agent' not in base_headers:
            raise ValueError("基础请求头中需要包含符合规范的 'user-agent' 字段")
        
        # 获取 tls 指纹...

        self.base_headers = base_headers.copy()
        self.cookies: Cookies = Cookies(cookies)
        self.proxies = proxies.copy() if proxies else None
        self.is_print = is_print

    def get(self, url: str, **kwargs) -> requests.Response:
        """发送 GET 请求"""
        return self._request("GET", url, **kwargs)

    def post(self, url: str, **kwargs) -> requests.Response:
        """发送 POST 请求"""
        return self._request("POST", url, **kwargs)
    
    def head(self, url: str, **kwargs) -> requests.Response:
        """发送 HEAD 请求"""
        return self._request("HEAD", url, **kwargs)
    
    def _prepare_headers(self, custom_headers: dict | None, cookies: str | list | None) -> dict:
        """合并基础头、自定义头、 cookies_str """
        headers = self.base_headers.copy()
        if custom_headers:
            headers.update(custom_headers)
            
        if cookies == None:
            cookies_str = self.cookies.get_cookies_str(self.cookies.get_keys())
        elif isinstance(cookies, str):
            cookies_str = cookies
        elif isinstance(cookies, list):
            cookies_str = self.cookies.get_cookies_str(cookies)
        else:
            raise TabError("cookies 类型错误")
        
        headers["cookie"] = cookies_str
        return headers

    def _request(
        self,
        method: str,
        url: str,
        headers: dict | None = None,
        cookies: str | list | None = None,
        value_handler=None,
        **kwargs
    ) -> requests.Response:
        """统一请求方法"""
        merged_headers = self._prepare_headers(headers, cookies)
        if self.is_print:
            logger.info(f"{method} {url}")
            logger.info(f"    headers: {merged_headers}")
            logger.info(f"    kwargs: {kwargs}")
            
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
            set_cookie_list = response.headers.get_list('Set-Cookie')
            value_handler = Request._deal_with_value_handler(value_handler)
            self.cookies.parse_set_cookie_of_headers(set_cookie_list, value_handler, self.is_print)
            
            return response
        except requests.RequestsError as e:
            raise RuntimeError(f"请求失败: {str(e)}") from e

    def set_cookie(self, key: str, value: str | None, expires=None, value_handler=None, cookie_value=None):
        '''设置 cookie, value 为 None 时, 对应 a=1; b; c=2 中 b 这样的 cookie '''
        value_handler = Request._deal_with_value_handler(value_handler)
        return self.cookies.set_cookie(key, value, expires, value_handler, False, cookie_value)
        
    def set_cookies(self, cookies, value_handler=None):
        '''批量设置 cookies'''
        value_handler = Request._deal_with_value_handler(value_handler)
        return self.cookies.set_cookies(cookies, value_handler)
        
    def delete_cookie(self, key):
        '''删除 self._cookies 中某条 cookie'''
        return self.cookies.delete_cookie(key)
        
    def get_cookie(self, key, has_property=False) -> str | bool | None | dict:
        '''获取 cookie 过期返回 False, 没有报错'''
        return self.cookies.get_cookie(key, has_property)

    def get_cookies_dict(self, has_property: bool = False, need_keys: list[str] = None) -> dict:
        '''获取 cookie 到 dict, 实现了深拷贝, need_keys 传入 None 是获取全部'''
        if need_keys == None:
            need_keys = self.cookies.get_keys()
        return self.cookies.get_cookies_dict(has_property, need_keys)

    def get_cookies_str(self, need_keys: list[str] = None) -> str:
        '''获取 cookie 到 str, need_keys 传入 None 是获取全部'''
        if need_keys == None:
            need_keys = self.cookies.get_keys()
        return self.cookies.get_cookies_str(need_keys)

    @staticmethod
    def _deal_with_value_handler(value_handler):
        '''处理 value_handler'''
        if value_handler == None:
            value_handler = lambda x: x 
        elif (value_handler != Request.quote) and (value_handler != Request.unquote):
            raise TypeError("value_handler 传入的类型错误")
        return value_handler
        
    @staticmethod
    def unquote(string: str | None):
        '''集成一份解码'''
        if string == None:
            return None
        
        if not isinstance(string, str):
            raise TypeError("string 需要传入一个 str")
        return unquote(string)
    
    @staticmethod
    def quote(string: str | None):
        '''集成一份编码'''
        if string == None:
            return None
        
        if not isinstance(string, str):
            raise TypeError("string 需要传入一个 str")
        return quote(string)
    
    @staticmethod
    def get_datetime(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        '''集成一份获取日期'''
        return CookieValue.get_datetime(days, seconds, microseconds, milliseconds, minutes, hours, weeks)

    @staticmethod
    def GMT2datetime(time_str):
        '''GMT 转为当前时区的 datetime'''
        return CookieValue.GMT2datetime(time_str)
    
    @staticmethod
    def dict2str(cookies: dict):
        '''将 cookie 的 dict 转化为 str , 如果 value 是 None, 就会只有 key'''
        return Cookies.dict2str(cookies)
    
    @staticmethod
    def str2dict(cookies: str):
        '''将 cookie 的 str 转化为 dict, 实现了深拷贝'''
        return Cookies.str2dict(cookies)
    
