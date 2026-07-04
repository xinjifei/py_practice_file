prices = [50.0, 52.5, 51.0, 54.2, 55.0, 53.5, 56.0]  # 模拟7个交易日收盘价
current_streak = 0
current_day = 0
max_streak = 0

for day, price in enumerate(prices, 1):
#涨跌幅
    if day == 1:
        change_rate = 0.00
    else:
        last_day_price = prices[day - 2]
        change_rate = (price - last_day_price) / last_day_price * 100

# 连续增长天数
    if change_rate > 0:
        current_streak += 1
        current_day += 1
    else:
        current_streak = 0
        current_day = 0

    #更新连胜
    if max_streak < current_streak:
        max_day = day
        max_streak = current_streak



    print(f"第{day}天价格{price:.2f},涨跌{change_rate:.2f}%，连续增长{current_streak}天")

#最终输出
print("---------")
print(f"最长连续上涨记录：{max_streak}天，结束于第{max_day}天")




