import time
import threading
import pyautogui
from pynput import keyboard

# 全局变量控制程序运行
is_running = False
click_interval = 0.1  # 点击间隔（秒），可自定义
click_button = 'left'  # 点击按键：left/right/middle


def auto_click():
    """自动点击核心函数"""
    global is_running
    print("自动点击已启动，按ESC键停止")
    while is_running:
        # 模拟鼠标点击：点击当前鼠标位置
        if click_button == 'left':
            pyautogui.click()
        elif click_button == 'right':
            pyautogui.rightClick()
        elif click_button == 'middle':
            pyautogui.middleClick()
        # 控制点击间隔
        time.sleep(click_interval)


def on_key_press(key):
    """键盘监听：ESC键启停"""
    global is_running
    try:
        if key == keyboard.Key.esc:
            if is_running:
                is_running = False
                print("自动点击已停止")
            else:
                is_running = True
                # 启动点击线程（避免阻塞键盘监听）
                click_thread = threading.Thread(target=auto_click)
                click_thread.daemon = True  # 主线程退出时子线程也退出
                click_thread.start()
    except Exception as e:
        print(f"按键监听出错：{e}")


def main():
    """程序主函数"""
    print("=== 通用自动点击程序（学习用）===")
    print("使用说明：")
    print("1. 运行程序后，将鼠标移到需要点击的位置")
    print("2. 按ESC键启动/停止自动点击")
    print("3. 关闭窗口可退出程序")
    print("===============================")

    # 设置pyautogui的防护：防止点击过快导致无法操作（可选）
    pyautogui.FAILSAFE = True  # 鼠标移到屏幕左上角可强制退出
    pyautogui.PAUSE = 0.01  # 每次操作的暂停时间

    # 启动键盘监听（阻塞式，保持程序运行）
    with keyboard.Listener(on_press=on_key_press) as listener:
        listener.join()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n程序已手动退出")
    except Exception as e:
        print(f"程序出错：{e}")