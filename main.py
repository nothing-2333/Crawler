import requests
from loguru import logger

from crawler import Crawler, Env, Encrypt, Request

debug = logger.debug


def run(env: Env, crawler: Crawler):
    debug("请求开始...")


if __name__ == "__main__":
    env = Env()
    base_headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }
    request = Request(base_headers)
    options = {
        "js": ["base.js"]
    }
    encrypt = Encrypt(options)
    crawler = Crawler(env, encrypt, request)

    run(env, crawler)

    