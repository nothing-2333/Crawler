import requests
from loguru import logger

from Crawler import Crawler
from Encrypt import Encrypt
from Env import Env, env


def run(crawler: Crawler, encrypt: Encrypt, env: Env):
    debug = crawler.debug
    debug("请求开始...")
    
    encrypt.test()

    

if __name__ == "__main__":
    session = requests.Session()
    crawler = Crawler(session, logger)
    encrypt = Encrypt(logger)

    run(crawler, encrypt)

    