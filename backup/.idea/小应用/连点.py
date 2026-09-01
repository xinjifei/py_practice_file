from pynput import mouse
import threading
import time
import logging

# 配置日志（仅关键信息）
logging.basicConfig(level=logging.WARNING, format='[%(time)s] %(message)s')

# 全局配置（可根据需求调整）
CLICK_INTERVAL = 0.01  # 点击间隔（秒），0.01=100次/秒，足够游戏使用且不卡顿
is_clicking = False
click_thread = None
mouse_controller = mouse.Controller()
event_lock = threading.Lock()


def auto_click():
    """优化后的连点函数：固定频率+低CPU占用"""
    global is_clicking
    while True:
        # 先检查状态，再执行点击，减少无效循环
        with event_lock:
            if not is_clicking:
                break

        try:
            # 模拟左键点击（简化为按下+松开，减少API调用次数）
            mouse_controller.press(mouse.Button.left)
            mouse_controller.release(mouse.Button.left)
        except Exception as e:
            logging.warning(f"点击执行异常：{e}")

        # 核心优化：固定间隔，让CPU有空闲处理游戏
        time.sleep(CLICK_INTERVAL)


def on_mouse_click(x, y, button, pressed):
    """鼠标事件回调（轻量化）"""
    global is_clicking, click_thread

    # 仅监听侧键X1（可改为X2）
    if button != mouse.Button.x1:
        return

    with event_lock:
        if pressed:
            if not is_clicking:
                is_clicking = True
                # 启动低优先级线程，减少与游戏抢资源
                click_thread = threading.Thread(target=auto_click)
                click_thread.daemon = True
                click_thread.name = "AutoClickThread"
                click_thread.start()
                print("✅ 开始连点（100次/秒）")
        else:
            is_clicking = False
            if click_thread and click_thread.is_alive():
                # 不强制等待线程结束，避免阻塞事件监听
                pass
            print("❌ 停止连点")


def set_thread_priority():
    """设置连点线程为低优先级（仅Windows生效）"""
    try:
        import psutil
        import os
        current_process = psutil.Process(os.getpid())
        # 设置进程优先级为“低于正常”
        current_process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
        print("✅ 已将程序设置为低优先级，减少游戏卡顿")
    except:
        # 非Windows系统/无psutil库则跳过，不影响核心功能
        pass


def main():
    print("=" * 60)
    print("我的世界专用连点器（低卡顿版）")
    print(f"当前连点频率：{1 / CLICK_INTERVAL:.0f}次/秒（可修改CLICK_INTERVAL调整）")
    print("1. 按住鼠标侧键（X1）开始连点，松开停止")
    print("2. 按 Ctrl+C 退出程序")
    print("=" * 60 + "\n")

    # 设置低优先级（优化卡顿关键）
    set_thread_priority()

    # 启动鼠标监听器（非阻塞模式，减少资源占用）
    listener = mouse.Listener(on_click=on_mouse_click)
    listener.start()

    try:
        # 主线程仅等待，不阻塞
        while listener.is_alive():
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n\n🛑 程序已手动终止")
        listener.stop()


if __name__ == "__main__":
    # 自动安装依赖
    required_packages = ['pynput']
    optional_packages = ['psutil']  # 用于设置进程优先级
    for pkg in required_packages + optional_packages:
        try:
            __import__(pkg)
        except ImportError:
            print(f"正在安装{pkg}库...")
            import subprocess
            import sys

            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

    main()