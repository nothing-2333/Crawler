import subprocess
import os
import json

class JsCall:
    def __init__(self, funcMap: dict) -> None:
        self.funcMap = funcMap
    
    def call(self, funcName: str, *args):
        paramStr = json.dumps(args)
        jsCode = self.funcMap[funcName] + ";" + "console.log(JSON.stringify({result:" + funcName + f"(...{paramStr})" + "}));"
        result = JsCall.runJs(jsCode)
        return json.loads(result)["result"]
    
    @staticmethod
    def load(fileName: str):
        workDirectory = os.getcwd() # 当前工作目录
        filePath = os.path.join(workDirectory, fileName) # 完整文件路径
        funcMap = JsCall.findFuncs(filePath)
        jsCall = JsCall(funcMap)
        return jsCall
    
    @staticmethod
    def findFuncs(filePath: str) -> dict:
        workDirectory = os.getcwd() # 当前工作目录
        findFuncPath = os.path.join(workDirectory, r"JsCall\findFunc.js") # 完整文件路径
        result = subprocess.run(['node', findFuncPath, filePath], capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data
        else:
            raise RuntimeError(result.stderr[:-1])
    
    @staticmethod
    def runJs(code: str) -> str:
        with subprocess.Popen(['node', '--trace-uncaught', '-'], 
        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True, encoding='utf-8') as proc:
            
            stdout, stderr = proc.communicate(input=code)
            if proc.returncode == 0:
                return stdout[:-1]
            else:
                raise RuntimeError(stderr[:-1])
        

if __name__ == "__main__":
    jsCall = JsCall.load("./Encrypt/encrypt.js")
    res = jsCall.call("jsonStringify", {"a": 2})
    print(res)
