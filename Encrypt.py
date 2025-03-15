# 自定义 python 加密，并融合 js加密

import json

from JsCall import JsCall

class Encrypt:
    def __init__(self, jsFilePaths) -> None:
        self.jsCall = JsCall.load(jsFilePaths)
    
    def jsonStringify(self, data):
        return self.jsCall.call("jsonStringify", data)
    

if __name__ == "__main__":
    e = Encrypt("encrypt/utils.js")
    print(e.jsonStringify({"a" : None}))
    