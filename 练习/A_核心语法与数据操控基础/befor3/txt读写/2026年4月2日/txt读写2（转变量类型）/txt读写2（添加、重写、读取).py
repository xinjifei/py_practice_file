'''
检测文件是否存在

如果不存在
    新建文件

存在
    while True：
        展示文件内容
        输入写入内容
        如果写入内容 = break
            break
            展示最后的文件内容
        展示写入内容
        循环

'''

import os

file_name = "int_to_str.txt"

#if os.path.exists(file_name): == false
if  not os.path.exists(file_name):
    with open("int_to_str.txt", "w", encoding="utf-8") as f:
        f.write("")

#if os.path.exists(file_name): == True

while True:
    with open("int_to_str.txt", "r", encoding="utf-8") as f:
        read = f.read()

    print(f'before rewrite value in <int_to_str.txt>={read}')


    input_value = input('input text\n>>>')

    #退出
    if input_value == "break":
        print(f'exit after rewrite value in <int_to_str.txt>={read}')
        break

    elif input_value == "quit":
        with open("int_to_str.txt", "w", encoding="utf-8") as f:
            f.write("")

    #写入
    else:
        with open("int_to_str.txt", "a", encoding="utf-8") as f:
            f.write(input_value)

        with open("int_to_str.txt", "r", encoding="utf-8") as f:
            read = f.read()

        print(f'after rewrite value in <int_to_str.txt>={read}')

