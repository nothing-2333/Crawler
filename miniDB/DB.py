import json
import os

class DB:
    def __init__(self):
        self.file_path = os.path.join(os.path.abspath(__file__), "..","data.json")

        with open(self.file_path, 'r') as file:
            self.data = json.load(file)

    def save(self):
        """
        将数据保存到 JSON 文件中。
        """
        with open(self.file_path, 'w') as file:
            json.dump(self.data, file, indent=4)
    
    def update(self, key, value):
        """
        更新或删除键值对。
        如果 value 是 None，则删除该键；否则更新或添加该键值对。
        """
        if value is None:
            self.data.pop(key, None)  # 如果键不存在，不会报错
        else:
            self.data[key] = value
    
    def clean(self):
        """
        删除所有数据。
        """
        self.data = {}
    
    def keys(self):
        """
        获取所有键。
        """
        return list(self.data.keys())
    
    def get(self, key):
        """
        根据键获取值。
        如果键不存在，返回 None。
        """
        return self.data.get(key)
    

# 示例用法
if __name__ == "__main__":
    db = DB()
    
    # 更新数据
    db.update("name", "Alice")
    db.update("age", 30)
    print(db.keys())
    print(db.get("name"))
    db.clean()
    print(db.data)
    db.save()
