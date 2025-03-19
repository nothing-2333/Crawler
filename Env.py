import json

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
        
        value = self.env[key]
        
        if len(value) == 1:
            return value[0]
        return value
    
    def download(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(self.env, file, ensure_ascii=False, indent=4)
    

env = Env()
