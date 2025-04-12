import json
import os
import random

class Env:
    def __init__(self, file_name=None):
        self.data = {}
        
        fingerprints_store_path = os.path.join(os.path.abspath(__file__), "..","fingerprints_store")
        if file_name == None:
            self.data_path = Env.getRandomJsonFile(fingerprints_store_path)
        else:
            self.data_path = os.path.join(fingerprints_store_path, file_name)

        self.loadFromJson(self.data_path)
        
    
    # 随机选择一个 .json 文件
    @staticmethod
    def getRandomJsonFile(directory):
        files = os.listdir(directory)
        json_files = [file for file in files if file.endswith('.json')]
        
        if not json_files:
            print("没有找到任何 .json 文件")
            return json_files
        
        random_json_file = random.choice(json_files)
        return os.path.join(directory, random_json_file)
    
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
    
    # 用 json 文件获取环境
    def loadFromJson(self, file_path):
        if not file_path.endswith(".json"):
            raise ValueError("这不是一个 JSON 文件")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        for key, value in data.items():
            self.update(key, value)


if __name__ == "__main__":
    for i in range(10): 
        env = Env()
        print(env.data)