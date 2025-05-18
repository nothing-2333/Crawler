from datetime import datetime, timedelta

class CookieValue:
    def __init__(self, value, expires):
        if value is None or isinstance(value, str):
            self.value = value
        else:
            raise ValueError("value 值不符合要求")
        
        if expires is None or isinstance(expires, str):
            self.expires = expires
        elif isinstance(expires, datetime):
            self.expires = str(expires)
        else:
            raise ValueError("expires 值不符合要求")

    def is_expired(self) -> bool:
        '''判断是否过期'''
        if self.expires:
            expires = datetime.strptime(self.expires, "%Y-%m-%d %H:%M:%S")
            if CookieValue.get_datetime() > expires:
                return True
        return False
    
    def get(self) -> dict:
        '''有属性就返回 dict, 否则返回 value'''
        if self.expires:
            return {
                "value": self.value,
                "expires": self.expires
            }
        else:
            return self.value
        
    @staticmethod
    def from_cookie_value(cookie_value: dict):
        '''以 dict 形式获取 CookieValue 实例的统一接口'''
        if "value" not in cookie_value:
            raise ValueError("必须包含 value")
        value = cookie_value["value"]
        if "expires" in cookie_value:
            expires = cookie_value["expires"]
        
        return CookieValue(value, expires)
    
    @staticmethod
    def get_datetime(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0) -> datetime:
        '''集成一份获取日期，只精确到秒'''
        target_time = datetime.now() + timedelta(days, seconds, microseconds, milliseconds, minutes, hours, weeks)
        return target_time.replace(microsecond=0)
    
    @staticmethod
    def GMT2datetime(time_str):
        '''GMT 转为当前时区的 datetime'''
        return datetime.strptime(time_str, "%a, %d %b %Y %H:%M:%S GMT")