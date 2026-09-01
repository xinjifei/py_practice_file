"""
操作>>>
for循环
    if 股票持有状态=hold
        放进持仓列表

    赋值：旧状态 = 更改前状态

    if price < 100
        执行调仓策略（状态更改为review）

    else ：
        执行调仓策略（状态更改为core）

    在调仓列表中添加字符串：添加的字符串 = 当前股票名称+当前股票价格+更改前状态（旧状态）+当前状态（经过调仓策略后的状态）

    if 状态 = core
        核心（core）状态统计计数变量 += 1
        核心（core）股票价格统计（用来算平均数） += 这次循环的股票价格

输出>>>
for 循环
    打印：持仓列表

for 循环
    打印：调仓列表

if 没有核心资产：
    赋值：核心资产平均价格变量 = 0

else：
    计算并赋值核心资产平均价格变量
    打印：核心资产数量并打印平均价格

"""

stock_pool = [
    {"code": "001", "name": "茅台", "price": 1800.0, "status": "hold"},
    {"code": "002", "name": "宁德", "price": 195.5, "status": "watch"},
    {"code": "003", "name": "比亚迪", "price": 260.0, "status": "hold"},
    {"code": "004", "name": "平安", "price": 45.2, "status": "hold"},
    {"code": "005", "name": "招行", "price": 32.8, "status": "watch"}
]

#赋值
hold_list = []
change_list = []
core_num = 0
core_price = 0


#操作>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
for stock in stock_pool:

    #判断并放进持仓列表
    if stock["status"] == "hold":
        hold_list.append(f"[持仓] {stock['name']}({stock['code']}) 现价: {stock['price']}")

    #保存旧状态
    old_status = stock["status"]

    #执行调仓策略
    if stock["price"] < 100:
        stock["status"] = "review"
    else:
        stock["status"] = "core"

    #在调仓列表中添加字符串
    change_list.append(f"[调仓]{stock['name']}({stock['code']})现价: {stock['price']}   |   状态：{old_status}->{stock['status']}")

    #统计核心资产
    if stock["status"] == "core":
        core_num += 1
        core_price += stock["price"]

#输出>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#输出持仓列表
print('>>> 初始持仓扫描')
for line in hold_list:
    print(line)

#输出调整后的列表
print(">>> 执行调仓逻辑")
for change in change_list:
    print(change)

#输出资产汇报
print("----------------")
print(">>> 核心资产统计")
print(f"核心资产数量: {core_num}, 平均价格: {core_price / core_num:.2f}")



'''
固定式输出：
>> 初始持仓扫描
[持仓] 茅台(001) 现价: 1800.00
[持仓] 比亚迪(003) 现价: 260.00
[持仓] 平安(004) 现价: 45.20
>>> 执行调仓逻辑
[调仓] 茅台(001) 现价: 1800.00 | 状态: hold -> core
[调仓] 宁德(002) 现价: 195.50 | 状态: watch -> core
[调仓] 比亚迪(003) 现价: 260.00 | 状态: hold -> core
[调仓] 平安(004) 现价: 45.20 | 状态: hold -> review
[调仓] 招行(005) 现价: 32.80 | 状态: watch -> review
----------------
>>> 核心资产统计
核心资产数量: 3, 平均价格: 751.83
'''






