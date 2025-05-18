from datetime import datetime

class CookieValue:
    def __init__(self, value, expires):
        if value is None or isinstance(value, str):
            self.value: str | None = value
        else:
            raise ValueError("value 值不符合要求")
        
        if expires is None or isinstance(expires, str):
            self.expires: datetime | None = expires
        else:
            raise ValueError("expires 值不符合要求")

    def is_expired(self) -> bool:
        '''判断是否过期'''
        if self.expires:
            expires = datetime.strptime(self.expires, "%Y-%m-%d %H:%M:%S.%f")
            if datetime.now() > expires:
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