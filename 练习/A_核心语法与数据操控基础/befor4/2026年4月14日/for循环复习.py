prices = [10.2, 10.5, 10.1, 10.8, 11.2, 10.9]
# 索引:   0     1     2     3     4     5
# 对应:  第1天 第2天 第3天 第4天 第5天 第6天
max_price = prices[0]
max_price_day = 1

for day, price in enumerate(prices, 1):
    if day == 1:
        change = 0.00

    else:
        last_day_price = prices[day - 2]
        change = price - last_day_price

    if price > max_price:
        max_price = price
        max_price_day = day

    print(f"第{day}天: 价格{price:.2f}, 涨跌{change:.2f}")
print("----------------")
print(f"最高价记录: {max_price:.2f}元 (出现在第{max_price_day}天)")

