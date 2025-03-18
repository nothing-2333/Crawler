import os

from rpc import Rpc

class Encrypt:
    def __init__(self):
        jscode = self.readCode("utils.js")
        self.js = Rpc()
        self.js.buildSocket(Rpc.serverOfJs, jscode)
    
    # 读取文件中代码
    def readCode(self, file_name):
        file_path = os.path.join(os.path.abspath(__file__), "..","encrypt", file_name)
        with open(file_path, "r", encoding="utf8") as file:
            content = file.read()
        return content
    
    # 测试
    def test(self):
        result = self.js.call("jsonStringify", {"a": 1, "b": 2})
        print(result)

if __name__ == "__main__":
    encrypt = Encrypt()
    encrypt.test()
    