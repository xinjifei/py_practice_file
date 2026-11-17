"""教师演示：用另一组数字追踪单资产现金账户。"""

# 起点：账户只有现金 200 元，没有股票。
cash = 200.0
shares = 0
price = 20.0

# 买入订单提出购买 4 股；这里额外假设订单全部按 20 元成交且无费用。
buy_order_shares = 4
cash -= buy_order_shares * price
shares += buy_order_shares

# 成交后，现金变为 120 元，持仓市值为 80 元，权益仍为 200 元。
equity = cash + shares * price
weight = shares * price / equity
print("买入成交：", "现金", cash, "股数", shares, "权益", equity, "权重", weight)

# 一张卖出 1 股的订单暂未成交，所以现金和股数都不变。
sell_order_shares = 1
print("卖出订单未成交：", "现金", cash, "股数", shares)

# 市场价格从 20 元变为 25 元；它改变市值和权益，却不改变股数和现金。
price = 25.0
equity = cash + shares * price
weight = shares * price / equity
print("价格上涨：", "现金", cash, "股数", shares, "权益", equity, "权重", weight)

# 前面的卖出订单现在按 25 元成交；这里只改变现金和股数，不再改变价格。
cash += sell_order_shares * price
shares -= sell_order_shares
equity = cash + shares * price
weight = shares * price / equity
print("卖出成交：", "现金", cash, "股数", shares, "权益", equity, "权重", weight)

# 在无费用、同一价格成交的假设下，卖出只把部分股票市值变成现金。
assert equity == 220.0
