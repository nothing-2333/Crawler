import socket
import json
import multiprocessing
import os
import subprocess
import time

class Rpc:
    def __init__(self):
        self.socket  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def __del__(self):
        self.close()
    
    # 调用
    def call(self, funcName, *args) -> str:
        # 处理参数
        data = {
            "funcName": funcName,
            "args": list(args)
        }
        data = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
        self.socket.sendall(data.encode('utf-8'))
        
        # 前 4 个字节是结果的长度
        length = self.socket.recv(4)
        length = int(length.decode('utf-8').strip())
        
        # 根据长度接受数据
        response = b""  
        while len(response) < length:
            chunk = self.socket.recv(1024)
            response += chunk
        
        response = json.loads(response.decode('utf-8'))
        if "result" in response:
            return response["result"]
        else:
            return None
    
    @staticmethod
    def get_random_free_port():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 0))
        port = s.getsockname()[1]
        s.close()
        return port
    
    # 建立本地 Socket
    def build_socket(self, server):
        # 分配一个随机空闲端口
        port = Rpc.get_random_free_port()
        
        self.process = multiprocessing.Process(target=server, kwargs={"port": port})
        self.process.daemon = True  # 设置为守护进程：主进程结束时，子进程也结束
        self.process.start()

        # 等待一会子线程启动
        time.sleep(0.5)

        self.socket.connect(('127.0.0.1', port))
        self.port = port
    
    # 关闭资源
    def close(self):
        if self.socket:
            self.socket.close()
            self.socket = None
        if self.process:
            self.process.terminate()  # 终止子进程
            self.process.join()  # 等待子进程完全退出
            self.process = None
            
    # 读取文件中代码
    @staticmethod
    def read_code(file_path):
        with open(file_path, "r", encoding="utf8") as file:
            content = file.read()
        return content
    
    # 运行制定 js 文件，启动 socket 服务
    @staticmethod
    def server_of_js(port):
        file_path = os.path.join(__file__, "..", "server-of-js.js")
        command = ["node", file_path, str(port)]
        subprocess.run(command, check=True)
    
    # 启动 js 的 RPC 服务
    @staticmethod
    def build_server_of_js(file_paths) -> "Rpc":
        jscode = ""
        for path in file_paths:
            jscode += Rpc.read_code(path)
            jscode += ";\n"
            
        js = Rpc()
        js.build_socket(Rpc.server_of_js)
        
        # 加载初始化代码
        js.call("eval", "let require = global.require;") # 正确处理 require
        js.call("eval", jscode)
        
        return js
            


