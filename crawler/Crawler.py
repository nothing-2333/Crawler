import inspect
import os
from types import FunctionType
import json

class Crawler:
    def __init__(self, requests, logger, request_dir_name="items") -> None:
        self.requests = requests
        self.logger = logger
        self.loadMethodsFromDirectory(request_dir_name)

    # 动态的为这个类添加方法
    def addMethod(self, method: FunctionType):
        if not isinstance(method, FunctionType):
            raise TypeError("需要传入一个函数。")
        setattr(self, method.__name__, method.__get__(self, type(self)))
    
    # 获取工作路径
    @staticmethod
    def getWorkDir():
        return os.path.join(os.path.abspath(__file__), "..", "..")
        
    # 将文件夹中所有文件的所有函数动态加载成类方法
    def loadMethodsFromDirectory(self, request_dir_name):
        work_dir = Crawler.getWorkDir()
        items_dir = os.path.join(work_dir, request_dir_name)
        for filename in os.listdir(items_dir):
            if filename.endswith(".py"):
                file_path = os.path.join(items_dir, filename)
                with open(file_path, "r", encoding="utf-8") as file:
                    file_content = file.read()
                # 使用 exec 动态执行文件内容
                namespace = {}
                exec(file_content, namespace)
                for obj in namespace.values():
                    if inspect.isfunction(obj):
                        self.addMethod(obj)

    # 下载数据封装
    @staticmethod
    def download(input_data, output_path: str):
        work_dir = Crawler.getWorkDir()
        output_path = os.path.join(work_dir, output_path)
        
        if isinstance(input_data, str):
            with open(output_path, "a", encoding='utf-8') as file:
                file.write(input_data + '\n')
        elif isinstance(input_data, bytes):
            with open(output_path, "ab") as file:
                file.write(input_data + b'\n')
        elif isinstance(input_data, dict):
            with open(output_path, 'a', encoding='utf-8') as file:
                json.dump(input_data, file, ensure_ascii=False, indent=4)
        else:
            raise TypeError("不支持的类型。只能下载 str|bytes|dict ，三种类型。")
if __name__ == "__main__":
    import requests
    crawler = Crawler(requests, 1, "items")
    
    def aaa(self, a):
        return a
    crawler.addMethod(aaa)
    print(crawler.aaa(1))
    crawler.test_method()