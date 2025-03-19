import requests
from loguru import logger

from Crawler import Crawler
from Encrypt import Encrypt


def run(crawler: Crawler, encrypt: Encrypt, **kwargs):
    debug = crawler.debug
    debug("请求开始...")
    
    encrypt.test()
    debug(kwargs)
    

if __name__ == "__main__":
    session = requests.Session()
    crawler = Crawler(session, logger)
    encrypt = Encrypt(logger)

    run(crawler, encrypt)

    