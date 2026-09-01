import sys
import subprocess
import time
import pyautogui
from pynput import keyboard
import tkinter as tk
from tkinter import ttk, messagebox

# ===================== 全局配置区（请根据自己的路径修改） =====================
# 1. SAI2相关配置
SAI2_PATH = r"D:\xiaoshu\SAI2.0\[Saier]SAI Ver.2\sai2"
IMAGE_PATH = r"C:\Users\ldy\Pictures\Screenshots"

# 2. 操作映射：数字键 -> (操作名称, 执行函数)
OPERATIONS = {
    '1': ('打开SAI2并加载草稿图', lambda: execute_sai2_operation()),
    '2': ('打开记事本', lambda: execute_notepad_operation()),
    '3': ('打开浏览器并访问百度', lambda: execute_browser_operation())
}
# =========================================================================

# 记录当前按下的键集合
current_keys = set()
# 全局监听器对象
listener = None


# ---------------------- 自动化操作函数 ----------------------
def execute_sai2_operation():
    """操作1：打开SAI2并加载指定图片"""
    try:
        print(f"[操作1] 正在打开SAI2：{SAI2_PATH}")
        subprocess.Popen([SAI2_PATH])
        time.sleep(3)  # 等待SAI2加载

        print("[操作1] 模拟按下 Ctrl+O 打开文件选择框...")
        pyautogui.hotkey('ctrl', 'o')
        time.sleep(1)

        print(f"[操作1] 输入图片路径：{IMAGE_PATH}")
        pyautogui.typewrite(IMAGE_PATH)
        time.sleep(0.5)
        pyautogui.press('enter')

        messagebox.showinfo("操作完成", "SAI2已打开并加载指定图片！")
        print("[操作1] 执行完成")

    except FileNotFoundError:
        err_msg = f"未找到SAI2程序，请检查路径：{SAI2_PATH}"
        messagebox.showerror("错误", err_msg)
        print(f"[操作1] 错误：{err_msg}")
    except Exception as e:
        err_msg = f"执行失败：{str(e)}"
        messagebox.showerror("错误", err_msg)
        print(f"[操作1] 错误：{err_msg}")


def execute_notepad_operation():
    """操作2：打开记事本"""
    try:
        print("[操作2] 正在打开记事本...")
        subprocess.Popen(['notepad.exe'])
        messagebox.showinfo("操作完成", "记事本已打开！")
        print("[操作2] 执行完成")
    except Exception as e:
        err_msg = f"执行失败：{str(e)}"
        messagebox.showerror("错误", err_msg)
        print(f"[操作2] 错误：{err_msg}")


def execute_browser_operation():
    """操作3：打开浏览器访问百度（默认Edge）"""
    try:
        print("[操作3] 正在打开浏览器访问百度...")
        subprocess.Popen(['msedge.exe', 'https://www.baidu.com'])
        messagebox.showinfo("操作完成", "浏览器已打开并访问百度！")
        print("[操作3] 执行完成")
    except Exception as e:
        err_msg = f"执行失败：{str(e)}"
        messagebox.showerror("错误", err_msg)
        print(f"[操作3] 错误：{err_msg}")


# ---------------------- 键盘监听函数 ----------------------
def on_press(key):
    """按键按下时的处理函数"""
    try:
        current_keys.add(key)
        # 处理字符键（数字/字母等）
        if hasattr(key, 'char') and key.char in OPERATIONS:
            print(f"检测到数字键 {key.char}，执行：{OPERATIONS[key.char][0]}")
            OPERATIONS[key.char][1]()  # 执行对应操作
    except:
        pass

    # 按ESC键退出程序
    if key == keyboard.Key.esc:
        print("检测到ESC键，退出程序...")
        root.quit()  # 关闭tkinter窗口
        return False


def on_release(key):
    """按键松开时的处理函数"""
    try:
        current_keys.remove(key)
    except KeyError:
        pass


# ---------------------- 可视化窗口函数 ----------------------
def create_gui():
    """创建tkinter可视化窗口"""
    global root
    root = tk.Tk()
    root.title("快捷键自动化工具")
    root.geometry("500x300")  # 窗口大小：宽500，高300
    root.resizable(False, False)  # 禁止调整窗口大小

    # 设置字体和样式
    style = ttk.Style()
    style.configure("Title.TLabel", font=("微软雅黑", 14, "bold"))
    style.configure("Content.TLabel", font=("微软雅黑", 10))

    # 标题标签
    title_label = ttk.Label(root, text="快捷键自动化操作面板", style="Title.TLabel")
    title_label.pack(pady=20)

    # 操作列表标签
    operation_text = "按下以下数字键执行对应操作：\n"
    for num, (name, _) in OPERATIONS.items():
        operation_text += f"【{num}】- {name}\n"
    operation_text += "\n【ESC键】- 退出程序"

    operation_label = ttk.Label(
        root,
        text=operation_text,
        style="Content.TLabel",
        justify="left"
    )
    operation_label.pack(pady=10, padx=20, anchor="w")

    # 提示标签
    tip_label = ttk.Label(
        root,
        text="提示：程序后台运行，按下数字键即可触发操作\n（窗口可最小化，不影响快捷键响应）",
        style="Content.TLabel",
        foreground="#666666"
    )
    tip_label.pack(pady=30)

    # 启动键盘监听器（非阻塞）
    global listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    # 窗口关闭时的处理
    def on_closing():
        if listener.is_alive():
            listener.stop()
        root.destroy()
        sys.exit(0)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


# ---------------------- 程序入口 ----------------------
if __name__ == "__main__":
    # pyautogui基础设置
    pyautogui.FAILSAFE = True  # 鼠标移到左上角可终止pyautogui操作
    pyautogui.PAUSE = 0.5  # 操作间隔0.5秒，避免过快

    # 启动可视化窗口
    create_gui()