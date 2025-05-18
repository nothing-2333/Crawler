import os
from loguru import logger

from .rpc import Rpc

debug = logger.debug

class Encrypt:
    def __init__(self, options=None):
        if options != None:
            self.build_server(options)
        
        self.options = options

    # 根据配置建立服务
    def build_server(self, options: dict):
        for sever_name, file_names in options.items():
            if sever_name == 'js':
                file_paths = []
                for file_name in file_names:
                    file_path = os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "impl", file_name))
                    file_paths.append(file_path)
                self.js = Rpc.build_server_of_js(file_paths)
            else:
                raise ValueError("暂不支持此服务。")
    # 测试
    def test(self):
        if self.js:
            result = self.js.call("test", {"a": 1, "b": 2})
            debug(result)

    