'''elif user_input == "search":

while True:
    print("<<<检索内容>>>")

    try:
        index = int(input("index（输入0退出）=\n>>>")) - 1
        if index == -1:
            print("已退出")
            break
        key = int(input("key=\n>>>"))

        if 0 <= index < len(_list) and 1 <= key <= 3:
            if key == 1:
                key = "key_1"
                print(f"处在列表中<{index + 1}>位的字典中对应键<{key}>的数值=<{_list[index][key]}>")

            elif key == 2:
                key = "key_2"
                print(f"处在列表中<{index + 1}>位的字典中对应键<{key}>的数值=<{_list[index][key]}>")

            elif key == 3:
                key = "key_3"
                print(f"处在列表中<{index + 1}>位的字典中对应键<{key}>的数值=<{_list[index][key]}>")

            else:
                print("输入需为1~3之间的整数")

        else:
            print("输入内容需要为已存在的列表数量或者")

    except ValueError:
        print("输入非法，输入有效数字")

        '''

_list = [
        {"key_1" : 1,"key_2" : 2,"key_3" : 3},
        {"key_1" : 4,"key_2" : 5,"key_3" : 6},
        { "key_1" : 7,"key_2" : 8, "key_3": 9}
    ]


def is_input_legal(f_index, f_key, f_len):

    try:
        if f_index == -1:
            return 1

        if 0 <= f_index < f_len and 1 <= f_key <= 3:
            return 2

        else:
            return 3

    except ValueError:
        return 4

while True:
    index = int(input("index（输入0退出）=\n>>>")) - 1
    iil = is_input_legal(index, key, len(_list))
    if iil == 1:
        print("已退出")
        break
    key =    int(input("key=\n>>>"))



    if iil == 2:
        if key == 1:
            key = "key_1"
            print(f"处在列表中<{index + 1}>位的字典中对应键<{key}>的数值=<{_list[index][key]}>")

        elif key == 2:
            key = "key_2"
            print(f"处在列表中<{index + 1}>位的字典中对应键<{key}>的数值=<{_list[index][key]}>")

        elif key == 3:
            key = "key_3"
            print(f"处在列表中<{index + 1}>位的字典中对应键<{key}>的数值=<{_list[index][key]}>")

    elif iil == 3:
        print("输入需为1~3之间的整数")

    else :
        print("输入非法，输入有效数字")

