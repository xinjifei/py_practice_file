"""教师演示：收盘后才知道的信号，只能从下一开盘起持有。"""

# 第一天收盘后才能得到完整收盘价和基于它的信号。
close_day_1 = 20.0
signal_after_close = True

# 第二天的开盘价和收盘价；开盘成交只是这里的明确假设。
open_day_2 = 23.0
close_day_2 = 25.0

# 原有账户在第一天收盘前已持有 1 股，所以承担隔夜价格变化。
old_shares = 1
old_overnight_pnl = old_shares * (open_day_2 - close_day_1)
old_intraday_pnl = old_shares * (close_day_2 - open_day_2)

# 新账户在信号出现时仍空仓，因此隔夜持仓收益是 0。
new_shares_before_open = 0
new_overnight_pnl = new_shares_before_open * (open_day_2 - close_day_1)

# 第二天开盘假设订单成交 1 股，才开始承担开盘到收盘的变化。
new_shares_after_open = 1 if signal_after_close else 0
new_intraday_pnl = new_shares_after_open * (close_day_2 - open_day_2)

# 对照两种持仓的收益区间，检查隔夜跳涨没有分给新买入者。
print("原有持仓：隔夜", old_overnight_pnl, "盘中", old_intraday_pnl)
print("新买入：隔夜", new_overnight_pnl, "盘中", new_intraday_pnl)

# 这些断言只是检查上述假设下的计算，没有证明现实中一定能开盘成交。
assert (old_overnight_pnl, old_intraday_pnl) == (3.0, 2.0)
assert (new_overnight_pnl, new_intraday_pnl) == (0.0, 2.0)
