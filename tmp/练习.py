while True:
    p = "shutdown"
    _input = input(">>>")
    if _input == "shutdown":
        print("成功")
    else:
        print(f"打错了，打成了{_input}")