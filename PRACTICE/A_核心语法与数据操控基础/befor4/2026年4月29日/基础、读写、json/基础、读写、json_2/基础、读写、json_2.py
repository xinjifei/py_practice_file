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

def read_json(file_name):
    with open (file_name, "r", encoding="utf-8") as f:
        return json.load(f)

def write_json(file_name, data):
    with open (file_name, "w", encoding="utf-8") as f1:
        json.dump(data, f1, ensure_ascii=False, indent=2)


stocks = "stock_list.json"

write_json(stocks, stock_list)

read_all = read_json(stocks)

total = 0
for line in read_all:
    print(line["name"], line["price"])
    total += line["price"]

print(f"更改前平均价 = {total / len(read_all):.3f}")

read_all = read_json(stocks)
for line, new in zip(read_all, new_price):
    line["price"] = new

write_json(stocks, read_all)

total = 0
for line in read_all:
    print(line["name"], line["price"])
    total += line["price"]

print(f"更改后平均价 = {total / len(read_all):.3f}")

