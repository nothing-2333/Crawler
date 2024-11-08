import requests
from loguru import logger
from Encrypt.Encrypt import Encrypt

class Crawler:
    def __init__(self) -> None:
        self.encrypt = Encrypt()
     
    def run(self):
        logger.debug("请求流程构建...")
        



if __name__ == "__main__":
    crawler = Crawler()
    crawler.run()