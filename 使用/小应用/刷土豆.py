import time
import threading
from pynput.mouse import Controller, Button
from pynput.keyboard import Listener, KeyCode

# ========== 参数配置 ==========
DELAY_START = 5
CYCLE_TIME = 1.5
RIGHT_PER_CYCLE = 5
LEFT_PER_CYCLE = 1
RIGHT_BEFORE_SCROLL = 64
SCROLL_TIMES = 8
SCROLL_DOWN = -5

mouse = Controller()
running = True  # 控制启停

def on_press(key):
    global running
    # 按 F6 退出
    if key == KeyCode.from_char('\x05') or key == KeyCode(vk=117):
        running = False
        print("\n🛑 F6 按下，程序停止")

# 启动键盘监听线程
listener = Listener(on_press=on_press)
listener.start()

def single_click(button):
    mouse.press(button)
    time.sleep(0.01)
    mouse.release(button)

print(f"⏳ {DELAY_START} 秒后开始，按 F6 可随时退出")
time.sleep(DELAY_START)

total_right = 0
scroll_count = 0

print("▶ 开始点击")

while running and scroll_count < SCROLL_TIMES:
    cycle_start = time.time()

    # 4次右键
    for _ in range(RIGHT_PER_CYCLE):
        if not running:
            break
        single_click(Button.right)
        total_right += 1

        if total_right % RIGHT_BEFORE_SCROLL == 0:
            mouse.scroll(0, SCROLL_DOWN)
            scroll_count += 1
            print(f"滚轮第 {scroll_count} 次")
            if scroll_count >= SCROLL_TIMES:
                break

    if not running or scroll_count >= SCROLL_TIMES:
        break

    # 1次左键
    single_click(Button.left)

    # 保证1.2秒一轮
    elapsed = time.time() - cycle_start
    if elapsed < CYCLE_TIME:
        time.sleep(CYCLE_TIME - elapsed)

print("✅ 程序已结束")
running = False
listener.stop()