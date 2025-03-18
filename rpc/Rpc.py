import socket
import json
import multiprocessing
import os

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
    
    # 建立本地 Socket
    def buildSocket(self, server, init_code="", port=2333):
        self.process = multiprocessing.Process(target=server)
        self.process.daemon = True  # 设置为守护进程：主进程结束时，子进程也结束
        self.process.start()

        self.socket.connect(('127.0.0.1', port))
        
        # 加载初始化代码
        self.call("eval", init_code)
    
    # 关闭资源
    def close(self):
        if self.socket:
            self.socket.close()
            self.socket = None
        if self.process:
            self.process.terminate()  # 终止子进程
            self.process.join()  # 等待子进程完全退出
            self.process = None
            
    # rpc 调用 js
    @staticmethod
    def serverOfJs():
        import subprocess
        file_path = os.path.join(__file__, "..", "serverOfJs.js")
        subprocess.run(["node", file_path], check=True)
        print(111)



if __name__ == "__main__":
    
    rpc = Rpc()
    rpc.buildSocket(Rpc.serverOfJs, "function a(){return 1;}")
    res = rpc.call("a", 1, 2)
    rpc.close()
    
    print(res)

