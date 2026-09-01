''''''

'''
def show_stock(name, price):
    print(f"股票：{name}，当前价格：{price}")

show_stock("宁德时代", 220)
'''

'''
def calculate(value1, value2):
    print(f"{value1}+{value2}={value1+value2}")

calculate(3, 5)
calculate(100, 200)
'''

'''
def change_rate(now, pre):
    _change = (now - pre) / pre * 100
    print(f"涨跌幅为{_change:.1f}%")

change_rate(10.5, 10)
'''

def stock_info(name, now, pre):
    _change = (now - pre) / pre * 100

    print(f"股票：{name}")
    print(f"昨日价格：{pre:.2f}")
    print(f"今日价格：{now:.2f}")
    print(f"涨跌幅：{_change:.2f}%")

stock_info("招商银行", 10.5, 10.0)

