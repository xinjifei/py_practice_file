'''def title():
    print("=====")
    print("基础、函数、综合练习")
    print("=====")
title()'''

'''def calc_fee(price, rate = 0.0003):
    fee = price * rate
    return fee
print(calc_fee(100))'''

'''def calc_change(pre, now):
    change_rate = (now - pre) / pre *100
    if change_rate == 0:
        state =  "平"
    elif change_rate > 0:
        state = "涨"
    else:
        state = "跌"
    print(f"涨跌幅={change_rate}，涨跌状态={state}")
    return change_rate, state

calc_change(100, 150)'''

def stock_report(name, now, pre, money = 100000, fee_rate = 0.0003):
    change_rate = (now - pre) / pre * 100
    if change_rate == 0:
        state = "平"
    elif change_rate > 0:
        state = "涨"
    else:
        state = "跌"

    calc_fee = money * fee_rate

    print(f'股票名称：{name}')
    print(f'昨日价格：{pre}')
    print(f'今日价格：{now}')
    print(f'涨跌幅：{change_rate:.4f}%')
    print(f'状态：{state}')
    print(f'交易金额：{money}')
    print(f'手续费：{calc_fee:.2f}')

stock_report("名字",1000, 900)















