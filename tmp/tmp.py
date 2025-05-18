from datetime import datetime

# 字符串表示的日期时间
a = "2025-05-18 12:05:02.809086"

# 使用 strptime 方法将字符串解析为 datetime 对象
date_format = "%Y-%m-%d %H:%M:%S.%f"
dt = datetime.strptime(a, date_format)

print(dt)  # 输出: 2025-05-18 12:05:02.809086
print(type(dt))  # 输出: <class 'datetime.datetime'>