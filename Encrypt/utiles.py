# 自定义 python 工具函数

def urlParse(url: str) -> dict:
    result = {}
    urlSplit = url.split("?")
    if len(urlSplit) == 2:
        for i in urlSplit[1].split("&"):
            result[i.split("=")[0]] = i.split("=")[1]
        return result
    else :
        return result

if __name__ == "__main__":
    print(urlParse("https://blog.csdn.net/qq_26917905/article/details/137969435"))
