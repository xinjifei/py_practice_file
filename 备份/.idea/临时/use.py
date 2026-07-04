

# ====================== 配置文件路径（项目根目录） ======================

import os
import time
import subprocess
import json

# ====================== 配置文件路径（项目根目录） ======================
JSON_FILE = "file_list.json"


# ====================== 读取 / 保存 JSON（双列表 修复版） ======================
def init_json():
    """初始化JSON结构，保证一定有 file_list 和 run_list"""
    if not os.path.exists(JSON_FILE):
        data = {
            "file_list": [{"xiaoshu": r"D:\xiaoshu"}],
            "run_list": []
        }
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return data

    with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "file_list" not in data:
        data["file_list"] = [{"xiaoshu": r"D:\xiaoshu"}]
    if "run_list" not in data:
        data["run_list"] = []

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return data


def load_file_list():
    data = init_json()
    return data["file_list"]


def load_run_list():
    data = init_json()
    return data["run_list"]


def save_file_list(file_list):
    data = init_json()
    data["file_list"] = file_list
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def save_run_list(run_list):
    data = init_json()
    data["run_list"] = run_list
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
# ====================== 主程序 ======================
def main():
    function_list = [
        "shutdown",
        "coding",
        "f",
        "r",
        "test"
    ]
    print("order list:")
    for i in function_list:
        print(f"<{i}>", end="  ")

    timeout = 30

    while True:
        start = time.time()
        user_input = ""

        while time.time() - start < timeout:
            try:
                user_input = input("\n>>> ").strip().lower()
                break
            except:
                time.sleep(0.5)
        else:
            return

        # ====================== 指令判断 ======================
        if user_input == "shutdown":
            os.system("shutdown /s /f /t 0")
            return

        elif user_input == "coding":
            print("    launching 3 app...")
            app_list = [
                r"D:\xiaoshu\python\py\PyCharm 2025.2.4\bin\pycharm64.exe",
                r"C:\Users\吕昌赫\AppData\Local\STranslate\current\STranslate.exe",
                r"C:\Users\吕昌赫\AppData\Local\Programs\Soda Music\SodaMusicLauncher.exe"
            ]
            for path in app_list:
                if os.path.isfile(path):
                    subprocess.Popen(path)
            return

        elif user_input == "test":
            os.system("start ms-settings:")
            return

        elif user_input == "f":
            file_list = load_file_list()
            print("    file_mode ")
            choos = input(">>> ")

            # -------------------- 查看所有路径 --------------------
            if choos == "check":
                print("    --- check mode ---")
                if not file_list:
                    print("    file list is empty")
                else:
                    for item in file_list:
                        key = list(item.keys())[0]
                        print(f"    key: {key}")
                continue

            # -------------------- 删除路径 --------------------
            elif choos == "del":
                print("    --- delete mode ---")
                del_key = input("    >>> ")
                found = False
                for item in file_list:
                    key = list(item.keys())[0]
                    if key == del_key:
                        file_list.remove(item)
                        save_file_list(file_list)
                        print(f"    delete success: {del_key}")
                        found = True
                        break
                if not found:
                    print(f"    key not found：{del_key}")
                continue

            # -------------------- 添加路径 --------------------
            elif choos == "add":
                print("    --- add mode ---")
                new_key = input("    key\n>>> ")
                new_value = input("    value\n>>> ")
                file_list.append({new_key: new_value})
                save_file_list(file_list)
                print(f"    add success: {new_key}")
                continue

            # -------------------- 打开路径 --------------------
            found = False
            for dic in file_list:
                key = list(dic.keys())[0]
                if choos == key:
                    os.startfile(dic[key])
                    found = True
                    return
            if not found:
                print(f"    key not found：{choos}")

        elif user_input == "r":
            run_list = load_run_list()  # 独立列表
            print("    run_mode ")
            choos = input(">>> ")

            # -------------------- 查看所有命令 --------------------
            if choos == "check":
                print("    --- check mode ---")
                if not run_list:
                    print("    run list is empty")
                else:
                    for item in run_list:
                        key = list(item.keys())[0]
                        print(f"    key: {key}")
                continue

            # -------------------- 删除命令 --------------------
            elif choos == "del":
                print("    --- delete mode ---")
                del_key = input("    >>> ")
                found = False
                for item in run_list:
                    key = list(item.keys())[0]
                    if key == del_key:
                        run_list.remove(item)
                        save_run_list(run_list)
                        print(f"    delete success: {del_key}")
                        found = True
                        break
                if not found:
                    print(f"    key not found：{del_key}")
                continue

            # -------------------- 添加命令 --------------------
            elif choos == "add":
                print("    --- add mode ---")
                new_key = input("    key\n>>> ")
                new_value = input("    value\n>>> ")
                run_list.append({new_key: new_value})
                save_run_list(run_list)
                print(f"    add success: {new_key}")
                continue

            # -------------------- 运行 PowerShell 命令 --------------------
            found = False
            for dic in run_list:
                key = list(dic.keys())[0]
                if choos == key:
                    cmd = dic[key]
                    subprocess.Popen(f"powershell -Command {cmd}", shell=True)
                    found = True
                    return
            if not found:
                print(f"    key not found：{choos}")

        else:
            print(f"    order <{user_input}> do not exists")


if __name__ == "__main__":
    main()