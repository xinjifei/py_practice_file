''''''
'''
定义三个函数
    csv读取
    txt写入
    json写入

从csv读取数据为列表中字典

进行计算
    总盈亏
    总投入成本
    整体收益率
    盈利最高股
    盈利最低股

计算后的结果写入txt文件

将csv中的数据遍历并以json格式写入json
'''

#导入库>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
import csv
import json

#函数定义>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def read_csv(file_name):
    data = []
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            csv_reader = csv.reader(f)
            next(csv_reader)
            for row in csv_reader:
                if len(row) < 4:
                    continue
                data.append(row)

    except FileNotFoundError as e:
        print(f"文件不存在，详见={e}")
    except Exception as e:
        print(f"未知错误，详见={e}")

    else:
        print("成功读取源文件")

    finally:
            print("文件读取流程结束")
    return data

def write_txt(file_name, data):
    try:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(data)

    except PermissionError as e:
        print(f"写入txt文件失败，原因权限不足，详见={e}")
    except Exception as e:
        print(f"写入txt文件失败，原因不明，详见={e}")

    else:
        print("写入txt文件成功")

    finally:
        print(f"执行日志导出成功，文件名={file_name}")

def write_json(file_name, data):
    try:
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    except PermissionError as e:
        print(f"写入json文件失败，原因权限不足，详见={e}")
    except Exception as e:
        print(f"写入json文件失败，原因未知，详见={e}")

    else:
        print("成功写入json文件")

    finally:
        print(f"结构化输出数据成功，文件名={file_name}")

#从csv读取数据为列表中字典>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
stock_list = []

for row in read_csv("stocks.csv"):
    try:
        hold = float(row[1])
        cost = float(row[2])
        price = float(row[3])
        if hold < 0 or cost < 0 or price < 0:
            print("数据中含有负数，跳过此行")
            continue

    except ValueError as e:
        print(f"类型转换错误，详见={e}")
        continue
    except Exception as e:
        print(f"未知错误，详见={e}")
        continue

    else:
        line = {"name": row[0], "hold": hold, "cost": cost, "price": price}
        print("存入内存列表成功")
        stock_list.append(line)

#判断股票数据临时列表是否合法>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
if not stock_list:
    print("临时股票存放列表为空，退出程序")
    exit()

#核心计算>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
all_pl = 0
all_cost = 0
#最值专用初始化赋值
first_stock = stock_list[0]
first_pl = (first_stock["price"] - first_stock["cost"]) * first_stock["hold"]
max_pl = first_pl
lowest_pl = first_pl
max_name = first_stock["name"]
lowest_name = first_stock["name"]

for stock in stock_list:
    #总盈亏
    pl = (stock["price"] - stock["cost"]) * stock["hold"]
    all_pl += pl
    #总投入成本
    all_cost += stock["cost"] * stock["hold"]
    #盈利最高股
    if pl > max_pl:
        max_pl = pl
        max_name = stock["name"]

    # 盈利最低股
    if pl < lowest_pl:
        lowest_pl = pl
        lowest_name = stock["name"]



#整体收益率
try:
    _yield = all_pl / all_cost * 100
except ZeroDivisionError as e:
    print(f"除数为零错误，详见={e}")
    _yield = 0
except Exception as e:
    print(f"未知错误，详见={e}")
    _yield = 0
all_cost_str = f"成本总计 = {all_cost:.2f}"
_yield_str = f"整体收益率 = {_yield:.2f}%"
max_pl_str = f"拥有最高盈利的股票名为 = {max_name}，（盈利={max_pl:.2f}）"
lowest_pl_str = f"拥有最低盈利的股票名为 = {lowest_name}，（盈利={lowest_pl:.2f}）"

#计算后的结果写入txt文件>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#总结列表初始化赋值
txt_list = []

#添加至txt列表
txt_list.append(all_cost_str)
txt_list.append(_yield_str)
txt_list.append(max_pl_str)
txt_list.append(lowest_pl_str)

content = "\n".join(txt_list)
write_txt("output.txt", content)

#将csv中的数据遍历并以json格式写入json>>>>>>>>>>>>>>>>>>>>>>>

#初始化赋值json列表
json_list = []

for stock in stock_list:
    #赋值
    line = {
        "name":stock["name"], "hold": float(stock["hold"]), "cost": float(stock["cost"]), "price": float(stock["price"])
    }
    #添加到json列表
    json_list.append(line)

#写入json文件
write_json("conversion.json", json_list)