import requests
from loguru import logger

from crawler import Crawler
from env import Env
from miniDB import miniDB

debug = logger.debug

if __name__ == "__main__":
    session = requests.Session()
    crawler = Crawler(session)
    crawler.encrypt.test()
    
    env = Env()
    debug(env.data)

    db = miniDB()
    
    # 更新数据
    db.update("name", "Alice")
    db.update("age", 30)
    print(db.keys())
    print(db.get("name"))
    db.clean()
    print(db.data)
    db.save()