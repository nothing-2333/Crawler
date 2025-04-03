import requests
from loguru import logger

from crawler import Crawler
from env import Env

debug = logger.debug

if __name__ == "__main__":
    session = requests.Session()
    crawler = Crawler(session)
    crawler.encrypt.test()
    
    env = Env()
    debug(env.data)

    