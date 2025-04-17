import requests
from loguru import logger

from crawler import Crawler
from env import Env
from miniDB import miniDB

debug = logger.debug

if __name__ == "__main__":
    crawler = Crawler({"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)..."})
    crawler.encrypt.test()
        
    env = Env()
    debug(env.fingerprints)

    db = miniDB()
    db.update("name", "Alice")
    db.update("age", 30)
    print(db.keys())
    print(db.get("name"))
    db.clean()
    print(db.data)
    db.save()