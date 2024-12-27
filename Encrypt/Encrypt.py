# 自定义 python 加密，并融合 js加密

import json
from JsCall import JsCall
from . import standard

class Encrypt:
    def __init__(self, filePath="./Encrypt/encrypt.js") -> None:
        self.standard = standard
        self.js = JsCall.load(filePath)
    
    def jsCall(self, *args):    # 懒人必备
        return self.js.call(*args)
    def baseCall(self, name, *args):
        return eval("self.standard." + name + "(*" + json.dumps(args) + ")")
    
    def jsonStringify(self, data):
        return self.jsCall("jsonStringify", data)
        
    def base64Encode(self, data):
        return self.baseCall("base64Encode", data)
    

if __name__ == "__main__":
    e = Encrypt()
    print(e.jsonStringify({"a" : None}))
    