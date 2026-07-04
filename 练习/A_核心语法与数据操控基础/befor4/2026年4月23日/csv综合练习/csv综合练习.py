''''''
'''
初始化股票源文件

从源文件逐行读取信息
计算读取的信息
将计算完成的信息添加至列表

新建result文件
写入表头
逐行写入经过计算的信息
'''

import csv

stocks = [
    ["股票名称", "成本价", "现价", "持仓"],
    ["贵州茅台", 1800, 1856, 100],
    ["比亚迪", 220, 235, 200],
    ["宁德时代", 160, 172, 300],
    ["中国平安", 48, 51, 500],
    ["招商银行", 32, 34, 400]
]

with open("source.csv", "w", encoding="utf-8", newline='') as f:
    writer = csv.writer(f)
    for stock in stocks:
        writer.writerow(stock)

with open("result.csv", "w", encoding="utf-8", newline='') as f1, open("source.csv", "r", encoding="utf-8") as f2:
    reader = csv.reader(f2)
    writer = csv.writer(f1)

    writer.writerow(["股票名称", "盈亏额"])

    next(reader)
    for row in reader:
        if not row:
            continue
        #计算盈亏
        cost = float(row[1])
        price = float(row[2])
        hold = float(row[3])

        pl = (price - cost) * hold

        writer.writerow([row[0], pl])



