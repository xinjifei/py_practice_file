import os



file_name = "int_to_str.txt"
default_list = [
        {"key_1" : 1,"key_2" : 2,"key_3" : 3},
        {"key_1" : 4,"key_2" : 5,"key_3" : 6},
        { "key_1" : 7,"key_2" : 8, "key_3": 9}
    ]

#空文件或空内容>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
if  not os.path.exists(file_name):
    print("<<<不存在文件，新建文件>>>")

    with open(file_name, "w", ) as f:
        f.write(str(default_list))


with open(file_name, "r") as f:
    read = f.read()

if read == "":
    read = str(default_list)

_list = eval(read)


while True:
    user_input = input("选择需要的功能###################\n>>>")

    # 放弃
    if user_input == "quit":
        print("<<<退出并清空内容>>>")

        with open(file_name, "w") as f:
            f.write(str(default_list))

            print("已退出并清除内容")
            break

    #退出>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    elif user_input == "bye":
        print("<<<退出并保存修改>>>")

        with open(file_name, "w") as f:
            f.write(str(_list))

        print("已退出程序并保存修改")

        with open(file_name, "r") as f:
            read = f.read()

            _list = eval(read)

            for i, key in enumerate(_list, 1):
                print(f"第{i}个字典：")
                print(f"键1={key['key_1']},键2={key['key_2']},键3={key['key_3']}")
        exit()

    #增加>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    elif user_input == "add":
        print("<<<添加内容>>>")

        try:
            key1 = int(input("key1=\n>>>"))
            key2 = int(input("key2=\n>>>"))
            key3 = int(input("key3=\n>>>"))

            new_dict = {"key_1":key1,"key_2":key2,"key_3":key3}

            _list.append(new_dict)

            with open(file_name, "w") as f:
                f.write(str(_list))

            print('成功更改')

        except ValueError:
            print("输入只能为整数")

    #删除>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    elif user_input == "del":

        while True:
            print("<<<删除内容>>>")

            try:
                index = int(input("要删除的字典的位数（输入0退出）=\n>>>")) - 1

                if index == -1:
                    print("已退出")
                    break

                elif   0 <= index < len(_list):
                    del _list[index]
                    with open(file_name, "w") as f:
                        f.write(str(_list))
                    print(f"成功删除了处于列表中第{index + 1}位的字典")
                    break

                else:
                    print("输入内容需要大于等于1并小于等于已存在的字典数量")

            except ValueError:
                print("输入非法，输入有效数字")

    #更改>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    elif user_input == "change":

        while True:
            print("<<<更改内容>>>")

            try:
                index = int(input("要更改的字典的位数（输入0退出）=\n>>>")) - 1

                if index == -1:
                    print("已退出")
                    break

                elif   0 <= index < len(_list):
                    change_1 = input("key1=\n>>>")
                    change_2 = input("key2=\n>>>")
                    change_3 = input("key3=\n>>>")

                    change_dict = {"key_1":change_1, "key_2":change_2, "key_3":change_3}

                    _list[index] = change_dict

                    with open(file_name, "w") as f:
                        f.write(str(_list))

                    print(f"成功更改了处于列表中第{index + 1}位的字典（更改后的字典）:\n"
                          f"{_list[index]}")
                    break

                else:
                    print("输入内容需要大于等于1并小于等于已存在的字典数量")

            except ValueError:
                print("输入非法，输入有效数字")

    #查看>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    elif user_input == "check":
        print("<<<查看内容>>>")

        for i, key in enumerate(_list, 1):
            print(f'第{i}个字典')
            print(f"键1={key['key_1']}，键2={key['key_2']}，键3={key['key_3']}")

   #检索>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    elif user_input == "search":

        while True:
            print("<<<检索内容>>>")

            try:
                index = int(input("index（输入0退出）=\n>>>")) - 1
                if index == -1:
                    print("已退出")
                    break
                key = int(input("key=\n>>>"))

                if   0 <= index < len(_list) and 1 <= key <= 3:
                    if key == 1:
                        key = "key_1"
                        print(f"处在列表中<{index+1}>位的字典中对应键<{key}>的数值=<{_list[index][key]}>")

                    elif key == 2:
                        key = "key_2"
                        print(f"处在列表中<{index+1}>位的字典中对应键<{key}>的数值=<{_list[index][key]}>")

                    elif key == 3:
                        key = "key_3"
                        print(f"处在列表中<{index+1}>位的字典中对应键<{key}>的数值=<{_list[index][key]}>")

                    else:
                        print("输入需为1~3之间的整数")

                else:
                    print("输入内容需要为已存在的列表数量或者")

            except ValueError:
                print("输入非法，输入有效数字")

    else:
        print("输入无效")



