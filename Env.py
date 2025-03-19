import json


class Env:
    def __init__(self):
        self.data = {}
    
    def has(self, key) -> bool:
        if key in self.data:
            return True
        else:
            return False
    
    def update(self, key, value):
        self.data[key] = value
    
    def get(self, key):
        if not self.has(key):
            return None
        return self.data[key]
    
    def download(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)
    
    # 用 json 文件加载实例
    @staticmethod
    def loadFromJson(file_path):
        env = Env()
        
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        for key, value in data.items():
            env.update(key, value)
            
        return env
