import requests
from loguru import logger
import os

from Crawler import Crawler
from Encrypt import Encrypt
from Env import Env


def run(env: Env, crawler: Crawler, encrypt: Encrypt):
    debug = crawler.debug
    debug("请求开始...")
    
    encrypt.test()
    debug(env.data)

    

if __name__ == "__main__":
    file_path = os.path.join(os.path.abspath(__file__), "..","env", "base.json")
    env = Env.loadFromJson(file_path)
    session = requests.Session()
    crawler = Crawler(session, logger)
    encrypt = Encrypt(logger)

    
    run(env, crawler, encrypt)

    