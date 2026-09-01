#导入命令行接收参数函数
import argparse

#创建接收器
parser = argparse.ArgumentParser(description="测试接收器")

#添加要接收的参数
parser.add_argument("num1", help="数字1")
parser.add_argument("num2", help="数字2")

#解析传入的参数
numbers = parser.parse_args()

#获取传入的参数
print("传入的参数=", numbers.num1, numbers.num2)