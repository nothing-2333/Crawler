from loguru import logger

from crawler import Crawler, Env, Encrypt, Request, dumps, loads, CookieValue, Cookies

debug = logger.debug



if __name__ == "__main__":
    env = Env()
    base_headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }
    request = Request(base_headers)
    options = {
        "js": ["base.js"]
    }
    encrypt = Encrypt(options)
    crawler = Crawler(env, encrypt, request)

    crawler.encrypt.test()
    crawler.request.set_cookie("aa", "aa==aa", Request.get_datetime(), Request.quote)

    print(crawler.request.has_cookie("aa"))
    print(crawler.request.has_cookie("bb"))
    
    
    
    a = dumps(crawler)
    crawler = loads(a)
    print(crawler.request.has_cookie("aa"))
   