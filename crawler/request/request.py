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
        
        # cookies 中我习惯存入已经 url 编码过的值
        self._cookies = {}
    
    @staticmethod
    def unquote(string: str):
        '''集成一份解码'''
        return unquote(string)
    
    @staticmethod
    def quote(string: str):
        '''集成一份编码'''
        return quote(string)
    
    def delete_cookie(self, key):
        '''删除 self._cookies 中某条 cookie'''
        if key in self._cookies:
            del self._cookies[key]

    @staticmethod
    def _is_correct_func_for_handling_cookie_str(func):
        '''判断穿的参数是否合规'''
        if func == Request.quote or func == Request.unquote:
            return True
        else:
            return False
        
    @staticmethod
    def cookies_dict_to_str(cookies: dict):
        '''将 cookie 的 dict 转化为 str , 如果 value 是 None, 就会只有 key'''
        if not isinstance(cookies, dict):
            raise TypeError("cookies 需要传入一个 dict")
        
        cookie_parts = []
        for key, value in cookies.items():
            if value != None:
                if not isinstance(value, str):
                    raise TypeError("cookie 的 value 值必须是 str 类型 或者 None。")
                cookie_parts.append(f"{key}={value}")
            else:
                cookie_parts.append(key)
        
        return "; ".join(cookie_parts)
    
    @staticmethod
    def cookies_str_to_dict(cookies: str):
        '''将 cookie 的 str 转化为 dict'''
        if not isinstance(cookies, str):
            raise TypeError("cookies 需要传入一个 str ")
        
        items = cookies.split(";")
        result = {}
        for item in items:
            cookie_list = item.strip().split("=", 1)
            if len(cookie_list) == 2:
                result[cookie_list[0]] = cookie_list[1]
            elif len(cookie_list) == 1:
                result[cookie_list[0]] = None 
            else:
                logger.warning(f"无法转成 dict 的 cookie: " + item)
                
        return result

    @staticmethod
    def handle_cookies_dict(cookies, need_keys: list=None, func=None):
        '''传进来一个 cookies dict 处理 need_keys func, 实现了深拷贝'''
        if not isinstance(cookies, dict):
            raise TypeError("cookies 需要传入一个 dict")
        
        result = {} # python 是引用传递, 要新建一个对象
        if need_keys == None:
            if func == None:
                result = cookies.copy()
            elif Request._is_correct_func_for_handling_cookie_str(func):
                for key, value in cookies.items():
                    result[func(key)] = func(value)
            else:
                raise TypeError("func 参数非法")
        elif isinstance(need_keys, list):
            for need_key in need_keys:
                if need_key not in cookies:
                    raise ValueError("need_keys 包含的 key 在 cookies 中找不到: ", need_key)
                else:
                    if func == None:
                        result[need_key] = cookies[need_key]
                    elif Request._is_correct_func_for_handling_cookie_str(func):
                        result[func(need_key)] = func(cookies[need_key])
                    else:
                        raise TypeError("func 参数非法")
        else:
            raise TypeError("need_keys 参数非法")
        
        return result

    def get_cookie(self, key, func=None):
        '''获取 cookie 可以设置是否编码、解码'''
        result = self._cookies[key]

        if func == None:
            return result
        elif Request._is_correct_func_for_handling_cookie_str(func):
            return func(result)
        else:
            raise TypeError("func 参数非法")
    
    def set_cookie(self, key, value, func=None):
        '''设置 cookie 可以设置是否编码、解码'''
        if not isinstance(value, str) and value is not None:
            raise TypeError("cookie 的 value 值必须是 str 类型 或者 None。")
        
        if Request._is_correct_func_for_handling_cookie_str(func):
            key = func(key)
            if value != None:
                value = func(value)
        elif func != None:
            raise TypeError("func 参数非法")
        
        self._cookies[key] = value

    def _get_cookies_dict(self, cookies=None, need_keys: list=None, func=None):
        '''获取 cookie 到 dict , 附带多个功能'''
        
        # 处理 cookies
        if cookies == None:
            cookies = self._cookies
        elif isinstance(cookies, str):
            cookies = Request.cookies_str_to_dict(cookies)
        else:
            raise TypeError("cookies 参数类型非法")
        
        # 处理 need_keys 和 func
        return Request.handle_cookies_dict(cookies, need_keys, func)

    def _get_cookies_str(self, cookies=None, need_keys: list=None, func=None):
        '''获取 cookie 到 str , 附带多个功能'''
        
        # 处理 cookies
        if cookies == None:
            cookies = self._cookies
            
        if not cookies:
            return ""
        
        # 处理 need_keys 和 func
        tmp = Request.handle_cookies_dict(cookies, need_keys, func)
        
        return Request.cookies_dict_to_str(tmp)
    
    def get_cookies(self, mode, cookies=None, need_keys: list=None, func=None):
        '''获取 cookies 的对外接口'''
        
        if mode == 'dict':
            return self._get_cookies_dict(cookies, need_keys, func)
        elif mode == 'str':
            return self._get_cookies_str(cookies, need_keys, func)
        else:
            return None

    def set_cookies(self, cookies, func=None):
        '''批量设置 cookies'''
        
        if isinstance(cookies, str):
            cookies = Request.cookies_str_to_dict(cookies)
        elif not isinstance(cookies, dict):
            raise TypeError("cookies 必须是 dict 或者 str ")

        for key, value in cookies.items():
            self.set_cookie(key, value, func)

    def _prepare_headers(self, custom_headers: Optional[Dict], cookies_str: str=None) -> Dict:
        """合并基础头与自定义头并组合进 cookies"""
        headers = self.base_headers.copy()
        if custom_headers:
            headers.update(custom_headers)
            
        if cookies_str == None:
            cookies_str = self.get_cookies("str")
        headers["cookie"] = cookies_str
            
        return headers

    def _request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict] = None,
        cookies_str: str | None = None,
        **kwargs
    ) -> requests.Response:
        """统一请求方法"""
        merged_headers = self._prepare_headers(headers, cookies_str)

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
            set_cookie_headers = response.headers.get_list('Set-Cookie')
            for set_cookie in set_cookie_headers:
                cookie_parts = set_cookie.split(';')
                name_value = cookie_parts[0].split('=', 1)
                name = name_value[0].strip()
                value = name_value[1].strip()
                logger.info(f"服务器设置 cookie: {name} -> {value}")
                self.set_cookie(name, value)
                
                for part in cookie_parts[1:]:
                    key, *values = part.split('=', 1)
                    key = key.strip()
                    if values:
                        value = values[0].strip()
                        if key.lower() == 'max-age':
                            # 将 Max-Age 的值从秒转换为小时
                            max_age_seconds = int(value)
                            max_age_hours = max_age_seconds / 3600
                            logger.info(f"    {key}: {max_age_hours:.2f}h")
                        else:
                            logger.info(f"    {key}: {value}")
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
    r = Request({'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'})
    
    
