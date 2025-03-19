import requests
from loguru import logger
import os

from Crawler import Crawler
from Encrypt import Encrypt
from Env import Env


def run(crawler: Crawler, encrypt: Encrypt, env: Env):
    debug = crawler.debug
    debug("请求开始...")
    
    encrypt.test()
    debug(env.data)

    

if __name__ == "__main__":
    session = requests.Session()
    crawler = Crawler(session, logger)
    encrypt = Encrypt(logger)
    file_path = os.path.join(os.path.abspath(__file__), "..","env", "base.json")
    env = Env.loadFromJson(file_path)
    
    run(crawler, encrypt, env)

    