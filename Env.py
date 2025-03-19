import json
import os

class Env:
    def __init__(self):
        self.env = {}
    
    def has(self, key) -> bool:
        if key in self.env:
            return True
        else:
            return False
    
    def add(self, key, value):
        if not self.has(key):
            self.env[key] = []
        self.env[key].append(value)
    
    def get(self, key):
        if not self.has(key):
            return None
        return self.env[key]
    
    # 从 json 文件中加载环境
    def loadFromJson(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        for key, value in data.items():
            self.add(key, value)
    
    def download(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(self.env, file, ensure_ascii=False, indent=4)
    

env = Env()
file_path = os.path.join(os.path.abspath(__file__), "..","env", "base.json")
env.loadFromJson(file_path)