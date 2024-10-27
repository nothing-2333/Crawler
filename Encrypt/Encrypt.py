# 自定义 python 加密，并融合 js加密

import execjs
from loguru import logger
from Base import *

def jsCall(*arg):
    with open("./Encrypt/Encrypt.js", 'r', encoding='UTF-8') as file:
        result = file.read()
    jsCode = execjs.compile(result)
    return jsCode.call(*arg)

def jSONStringify(jsonData):
    return jsCall("jSONStringify", jsonData)


if __name__ == "__main__":
    logger.debug(base64Encode("nothing"))
    logger.debug(jsCall("jSONStringify", {"a" : None}))
    