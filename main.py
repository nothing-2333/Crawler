import requests

from Encrypt import Encrypt

class Crawler:
    def __init__(self) -> None:
        self.encrypt = Encrypt("encrypt/utils.js")
     
    def run(self):
        print(self.encrypt.jsonStringify({"a" : None}))
        print("请求流程构建...")


if __name__ == "__main__":
    crawler = Crawler()
    crawler.run()