import requests
from loguru import logger

from crawler import Crawler
from Encrypt import Encrypt


def run(crawler: Crawler, encrypt: Encrypt):
    crawler.logger.debug("请求开始...")
    encrypt.test()
    

if __name__ == "__main__":
    crawler = Crawler(requests, logger)
    encrypt = Encrypt()
    run(crawler, encrypt)

    