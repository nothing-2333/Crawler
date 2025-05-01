import json
import os
import random
from loguru import logger


class Env:
    def __init__(self, fingerprints_file_name=None):
        self.fingerprints = {}
        
        self.fingerprints_file_name = fingerprints_file_name
        self.fingerprints_path = Env._get_file_path("fingerprints-store", fingerprints_file_name)
        logger.info(f"选择环境文件 ---> {self.fingerprints_path}")
        
        Env.load_from_json(self.fingerprints, self.fingerprints_path)
    
    def get(self, key):
        return self.fingerprints.get(key, None)
    
    def get_fingerprints_file_name(self) -> str:
        '''获取选择环境的文件名'''
        if self.fingerprints_file_name == None:
            self.fingerprints_file_name = os.path.basename(self.fingerprints_path)
        return self.fingerprints_file_name
            
    # 获取要加载的文件路径：若没指定就随机选择
    @staticmethod
    def _get_file_path(dir_name, file_name=None):
        dir_path = os.path.abspath(os.path.join(os.path.abspath(__file__), "..", dir_name))
        if file_name == None:
            file_path = Env.get_random_json_file(dir_path)
        else:
            file_path = os.path.join(dir_path, file_name)
        return file_path
        
    # 随机选择一个 .json 文件
    @staticmethod
    def get_random_json_file(directory):
        files = os.listdir(directory)
        json_files = [file for file in files if file.endswith('.json')]
        
        if not json_files:
            print("没有找到任何 .json 文件")
            return json_files
        
        random_json_file = random.choice(json_files)
        return os.path.join(directory, random_json_file)
    
    # 用 json 文件获取环境
    @staticmethod
    def load_from_json(obj: dict, file_path: str):
        # 检查文件路径是否以 .json 结尾
        if not file_path.endswith(".json"):
            raise ValueError("这不是一个 JSON 文件")
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件 {file_path} 不存在")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        obj.update(data)


if __name__ == "__main__":
    for i in range(10): 
        env = Env()
        print(env.fingerprints)