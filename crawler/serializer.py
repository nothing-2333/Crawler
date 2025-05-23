import json

from .encrypt import Encrypt
from .request import Request
from .env import Env
from .crawler import Crawler


def dumps(crawler: Crawler, targets: list = []) -> str:
    '''将实例输出为字符串 json'''
    data = {}
    if targets:
        if isinstance(crawler.env, Env) and crawler.env in targets:
            data['env'] = {
                "fingerprints_file_name": crawler.env.get_fingerprints_file_name()
            }
        if isinstance(crawler.encrypt, Encrypt) and crawler.encrypt in targets:
            data['encrypt'] = {
                "options": crawler.encrypt.options
            }
        if isinstance(crawler.request, Request) and crawler.request in targets:
            data["request"] = {
                "base_headers": crawler.request.base_headers,
                "cookies": crawler.request.get_cookies_dict(True),
                "proxies": crawler.request.proxies,
                "is_print": crawler.request.is_print
            }
    else:
        if isinstance(crawler.env, Env):
            data['env'] = {
                "fingerprints_file_name": crawler.env.get_fingerprints_file_name()
            }
        if isinstance(crawler.encrypt, Encrypt):
            data['encrypt'] = {
                "options": crawler.encrypt.options
            }
        if isinstance(crawler.request, Request):
            data["request"] = {
                "base_headers": crawler.request.base_headers,
                "cookies": crawler.request.get_cookies_dict(True),
                "proxies": crawler.request.proxies,
                "is_print": crawler.request.is_print
            }
    data["tmp"] = crawler.tmp
    
    return json.dumps(data, ensure_ascii=False, indent=4)

def loads(data: str) -> Crawler:
    '''从字符串 json 加载实例'''
    data = json.loads(data)
    crawler = Crawler()
    if 'env' in data:
        crawler.env = Env(data['env']["fingerprints_file_name"])
    if 'encrypt' in data:
        crawler.encrypt = Encrypt(data['encrypt']["options"])
    if 'request' in data:
        crawler.request = Request(data["request"]["base_headers"], data["request"]["cookies"], data["request"]["proxies"], data["request"]["is_print"])
    crawler.tmp = data["tmp"]
    
    return crawler