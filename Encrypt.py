import os

from rpc import Rpc

class Encrypt:
    def __init__(self, logger):
        self.logger = logger
        self.debug = logger.debug
        self.error = logger.error
        
        # 用 js 测试，不用的话可以换成别的
        file_path = os.path.join(os.path.abspath(__file__), "..","encrypt", "base.js")
        self.js = Rpc.buildServerOfJs([file_path], 2333)

    # 测试
    def test(self):
        result = self.js.call("jsonStringify", {"a": 1, "b": 2})
        self.debug(result)

if __name__ == "__main__":
    from loguru import logger
    encrypt = Encrypt(logger)
    encrypt.test()
    