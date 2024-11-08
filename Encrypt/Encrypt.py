# 自定义 python 加密，并融合 js加密

import sys
import os
import json

class Encrypt:
    def __init__(self, filePath="./Encrypt/encrypt.js") -> None:
        # 将文件加入搜索路径
        Encrypt.appendSearch("JsCall")
        Encrypt.appendSearch("Encrypt")
        from JsCall import JsCall
        import base
        
        self.base = base
        self.js = JsCall.load(filePath)
    
    @staticmethod
    def appendSearch(fileName):
        jsCallPath = os.path.abspath(os.path.join(os.getcwd(), fileName))
        if jsCallPath not in sys.path:
            sys.path.append(jsCallPath)
    
    def jsCall(self, *args):    # 懒人必备
        return self.js.call(*args)
    def baseCall(self, name, *args):
        return eval("self.base." + name + "(*" + json.dumps(args) + ")")
    
    def jsonStringify(self, data):
        return self.jsCall("jsonStringify", data)
        
    def base64Encode(self, data):
        return self.baseCall("base64Encode", data)
    

if __name__ == "__main__":
    e = Encrypt()
    print(e.baseAndMD5("nothing"))
    print(e.jsonStringify({"a" : None}))
    