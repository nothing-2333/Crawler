import requests
from loguru import logger
from Encrypt.Encrypt import Encrypt

class Crawler:
    def __init__(self) -> None:
        pass
    
    def run(self):
        logger.debug("请求流程构建...")



if __name__ == "__main__":
    crawler = Crawler()
    crawler.run()
    e = Encrypt()
    print(e.base64Encode("nothing"))
    print(e.jsonStringify({"a" : None}))