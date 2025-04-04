import os
from loguru import logger

from ..rpc import Rpc

debug = logger.debug

class Encrypt:
    def __init__(self):
        # 用 js 测试，不用的话可以换成别的
        file_path = os.path.join(os.path.abspath(__file__), "..", "impl", "base.js")
        self.js = Rpc.buildServerOfJs([file_path])

    # 测试
    def test(self):
        result = self.js.call("test", {"a": 1, "b": 2})
        debug(result)

    