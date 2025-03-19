class MyClass:
    def __new__(cls, *args, **kwargs):
        print(f"__new__ called with: cls={cls}, args={args}, kwargs={kwargs}")
        instance = super().__new__(cls)
        return instance

    def __init__(self, value, name="default"):
        print(f"__init__ called with: self={self}, value={value}, name={name}")
        self.value = value
        self.name = name

# 创建实例
obj = MyClass(10, name="Alice")