'''第 1 天 练习题目
必须使用知识点：
with open() 语句
readlines() 读取文本
write() 单行写入
相对路径

输入要求：
在程序同一目录下新建 stock_list.txt，每行存放一只股票名称。

输出要求：
从 stock_list.txt 读取股票名称
为每只股票模拟一个盈亏金额
计算所有股票的总盈亏
将每只股票名称 + 盈亏金额按行写入 result.txt
在文件最后一行写入总盈亏
每条信息单独占一行'''

'''
新建result文件

循环
    如果这一行没有内容
        将总盈亏值放进result文件夹的最后一行
        break
    
    读取每一行的股票名
    将名字以及一个随机数添加到result文件夹的一行
    将随机数相加最后得到盈亏值总数
'''
import random
all_pl = 0

with open('result.txt', 'w') as f:
    f.write("")

with open('stock_list.txt', 'r', encoding="utf-8") as f1, \
    open('result.txt', 'w', encoding="utf-8")as f2:

    for line in f1.readlines():
        line = line.strip()
        pl = random.randint(-50,100)
        if not line:  # 跳过空行
            continue

        f2.write(f"股票名称={line}，盈亏={pl}\n")
        all_pl += pl

    f2.write(f"总盈亏额={all_pl}")

