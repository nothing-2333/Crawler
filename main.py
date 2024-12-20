import requests
from Encrypt import Encrypt

class Crawler:
    def __init__(self) -> None:
        self.encrypt = Encrypt()
     
    def run(self):
        self.encrypt.base64Encode("asd")
        print("请求流程构建...")


if __name__ == "__main__":
    crawler = Crawler()
    crawler.run()