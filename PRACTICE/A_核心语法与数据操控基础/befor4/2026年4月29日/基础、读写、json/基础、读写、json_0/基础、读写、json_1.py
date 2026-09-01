#导入json读写库
import json

#准备字典数据（单字典）
stock = {
    "name": "贵州茅台",
    "code": "600519",
    "price": 1790.50,
    "desc": "白酒龙头"
}

#创建并写入数据到json文件
file = "stock.json"
with open(file, "w", encoding="utf-8") as f:
    json.dump(stock, f , ensure_ascii=False, indent=2)

#读取文件内容
with open(file, "r", encoding="utf-8") as f:
    read = json.load(f)

print(read)
print(type(read))
print(read["name"])
