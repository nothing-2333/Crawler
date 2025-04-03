import socket

def get_random_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    
    return port

# 获取一个随机的空闲端口
free_port = get_random_free_port()
print(f"随机获取的空闲端口是: {free_port}")