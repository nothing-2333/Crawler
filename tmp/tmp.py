import os
import random

def get_random_json_file(directory):
    # 获取指定目录下的所有文件和文件夹
    files = os.listdir(directory)
    
    # 筛选出所有以 .json 结尾的文件
    json_files = [file for file in files if file.endswith('.json')]
    
    # 如果没有找到任何 .json 文件，返回 None
    if not json_files:
        print("没有找到任何 .json 文件")
        return json_files
    
    # 随机选择一个 .json 文件
    random_json_file = random.choice(json_files)
    
    # 返回文件的完整路径
    return os.path.join(directory, random_json_file)

# 指定路径
directory_path = os.path.join(os.path.abspath(__file__), "..")

# 获取随机的 .json 文件
random_json_file_path = get_random_json_file(directory_path)

print(f"随机选择的 .json 文件路径是: {random_json_file_path}")