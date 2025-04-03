import requests
from loguru import logger
import os

from Crawler import Crawler
from env import Env


def run(env: Env, crawler: Crawler):
    debug = crawler.debug
    debug("请求开始...")

    debug(env.data_path)

    

if __name__ == "__main__":
    env = Env()
    
    session = requests.Session()
    crawler = Crawler(session, logger)
    
    run(env, crawler)

    