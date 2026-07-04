import time
from pynput.mouse import Controller

mouse = Controller()

# 配置
interval = 185   # 每185秒滚一次
total = 8        # 共8次

print(f"开始运行，{interval}秒滚动一次，共{total}次")

for i in range(1):

    time.sleep(interval)


for i in range(total):
    print(f"第 {i+1} 次向下滚动")
    mouse.scroll(0, -3)  # 向下滚（负数=下，正数=上，数字越大滚越多）

    if i < total - 1:
        time.sleep(interval)

print("结束！")