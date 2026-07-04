#导入读写库
import json

stock_list = [
    {"name":"贵州茅台", "price":1790.5},
    {"name":"比亚迪", "price":258.2},
    {"name":"宁德时代", "price":185.6}
]

new_price = [
    4321.3,
    312.3,
    321.5
]

stocks = "stock_list.json"

with open(stocks, "w", encoding="utf-8") as f:
    json.dump(stock_list, f , ensure_ascii=False, indent=2)

with open (stocks, "r", encoding="utf-8") as f1:
    read_all = json.load(f1)

total = 0
for line in read_all:
    print(line["name"], line["price"])
    total += line["price"]

print(f"更改前平均价 = {total / len(read_all):.3f}")

with open (stocks, "r", encoding="utf-8") as f2:
    read_all = json.load(f2)

    for line, new in zip(read_all, new_price):
        line["price"] = new

with open (stocks, "w", encoding="utf-8") as f3:
    json.dump(read_all, f3, ensure_ascii=False, indent=2)

total = 0
for line in read_all:
    print(line["name"], line["price"])
    total += line["price"]

print(f"更改后平均价 = {total / len(read_all):.3f}")



