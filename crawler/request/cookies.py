from loguru import logger

from .cookie_value import CookieValue

class Cookies:
    def __init__(self, cookies=None):
        # 处理 cookies, 默认储存编码过的, 以 dict 形式储存
        self._cookies: dict[str, CookieValue] = {}
        if cookies is not None:
            self.set_cookies(cookies, lambda x: x)
            
    
    def get_keys(self):
        '''获取全部的键值'''
        return self._cookies.keys()
    
    def set_cookie(self, key: str, value: str | None, expires, value_handler, is_print, cookie_value=None):
        '''设置 cookie, value 为 None 时, 对应 a=1; b; c=2 中 b 这样的 cookie '''
        # cookie_value 用来设置更多的属性, 并降低与 cookie_value.py 的耦合
        if cookie_value == None:
            value = value_handler(value)
            self._cookies[key] = CookieValue(value, expires)
            if is_print:
                logger.info(f"设置 cookie: {key} -> {value}")
                if expires:
                        logger.info(f"    expires: {expires}")
        else:
            if "value" not in cookie_value:
                raise ValueError("必须包含 value")
            else:
                cookie_value["value"] = value_handler(cookie_value["value"])
                self._cookies[key] = CookieValue.from_cookie_value(cookie_value)
                if is_print:
                    logger.info(f"设置 cookie: {key} -> {cookie_value['value']}")
                    if 'expires' in cookie_value:
                            logger.info(f"    expires: {cookie_value['expires']}")
    
    def set_cookies(self, cookies: str | dict, value_handler):
        '''批量设置 cookies'''
        if isinstance(cookies, str):
            cookies = Cookies.str2dict(cookies)
            for key, value in cookies.items():
                self.set_cookie(key, value, None, value_handler, False)
        elif isinstance(cookies, dict):
            for key, value in cookies.items():
                if isinstance(value, str) or value is None:
                    self.set_cookie(key, value, None, value_handler, False)
                if isinstance(value, dict):
                    self.set_cookie(key, None, None, value_handler, False, cookie_value=value)
        else:
            raise TypeError("cookies 必须是 dict 或者 str ")
    
    def delete_cookie(self, key):
        '''删除 self._cookies 中某条 cookie'''
        if key in self._cookies:
            del self._cookies[key]
            
    def get_cookie(self, key, has_property: bool) -> str | bool | None | dict:
        '''获取 cookie 过期返回 False, 没有报错'''
        cookie_value = self._cookies[key]
        if cookie_value.is_expired():
            return False
        else:
            if has_property:
                return cookie_value.get()
            else:
                return cookie_value.value
        
    def get_cookies_dict(self, has_property: bool, need_keys: list[str]) -> dict:
        '''获取 cookie 到 dict, 实现了深拷贝'''
        result = {}
        
        for need_key in need_keys:
            value = self.get_cookie(need_key, has_property)
            result[need_key] = value
            
        return result

    def get_cookies_str(self, need_keys: list[str]) -> str:
        '''获取 cookie 到 str'''
        cookies_dict = self.get_cookies_dict(False, need_keys)
        return Cookies.dict2str(cookies_dict)
    
    def parse_set_cookie_of_headers(self, set_cookie_list: list[str], value_handler, is_print):
        '''解析请求头的 Set-Cookie 字段'''
        for set_cookie in set_cookie_list:
            cookie, *property = set_cookie.split(';', 1)
            
            # 先处理 cookie
            cookie = Cookies.str2dict(cookie)
            key = list(cookie.keys())[0] # cookie.keys() 必然只有一个
            value = cookie[key]
            
            expires = None
            # 再处理属性
            if property:
                property = Cookies.str2dict(property[0])
                for property_name, property_value in property.items():
                    
                    if property_name.lower() == 'max-age':
                        expires = CookieValue.get_datetime(seconds=int(property_value))

                    if expires == None and property_name.lower() == 'expires': # 'max-age' 优先级更高
                        expires = CookieValue.GMT2datetime(property_value)
            
            self.set_cookie(key, value, expires, value_handler, is_print)

            
    @staticmethod
    def dict2str(cookies: dict):
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
    def str2dict(cookies: str):
        '''将 cookie 的 str 转化为 dict, 实现了深拷贝'''
        if not isinstance(cookies, str):
            raise TypeError("cookies 需要传入一个 str ")
        
        items = cookies.split(";")
        result = {}
        for item in items:
            key, *values = item.split("=", 1)
            key = key.strip()
            if values:
                result[key] = values[0].strip()
            else:
                result[key] = None
                       
        return result
    
