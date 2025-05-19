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
    crawler.request.set_cookie("aa", "aa==aa", Request.get_datetime(days=5), Request.quote)

    gmt_time_str = "Mon, 26 May 2025 12:30:45 GMT"

    crawler.request.set_cookie("bb", None, Request.GMT2datetime(gmt_time_str), Request.quote)
    
    print(crawler.request.get_cookie("bb"))
    
    a = dumps(crawler)
    print(a)
   