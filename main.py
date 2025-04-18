import requests
from loguru import logger

from crawler import Crawler
from env import Env
from miniDB import miniDB

debug = logger.debug


def run(env: Env, crawler: Crawler):
    debug("请求开始...")


if __name__ == "__main__":
    env = Env()
    db = miniDB()
    
    session = requests.Session()
    crawler = Crawler(session)
    
    run(env, crawler)

    