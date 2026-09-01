



ceiling = 10000
a = 1
b = 2
c = 3

file_name = "list_generated.txt"
_list = [{"key_1": 1, "key_2": 2, "key_3": 3}]



while True:
    user_input = input("选择功能\n>>>")

    if user_input == "add":
        count = 0
        while True:#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            a += 3
            b += 3
            c += 3

            new_dict = {"key_1": a, "key_2": b, "key_3": c}

            _list.append(new_dict)

            with open(file_name, "w") as f:
                f.write(str(_list))

            print(new_dict)

            count += 1
            if count > ceiling:
                break

    elif user_input == "del":
        with open(file_name, "w") as f:
            f.write("")

    else:
        print("输入功能")
