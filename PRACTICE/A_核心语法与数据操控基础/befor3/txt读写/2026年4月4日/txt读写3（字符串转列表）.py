'''
检测文件是否存在

如果不存在
    新建文件

存在
    while True：
        展示文件内容
        输入写入内容
        如果写入内容 = break
            exit()

            展示最后的文件内容
        展示写入内容
        循环

'''

import os


stocks = [{"code": "00001","name": "name_a","price": 0,"change": 0},
          {"code": "00002","name": "name_b","price": 0,"change": 0},
          {"code": "00003","name": "name_c","price": 0,"change": 0},
          {"code": "00004","name": "name_d","price": 0,"change": 0}]

file_name = "str_ditc.txt"

if not os.path.exists(file_name):
    with open("str_ditc.txt", mode="w", encoding="utf-8") as f:
        f.write(str(stocks))

while True:
    with open(file_name,mode="r",encoding="utf-8") as f:
        read= f.read()

        stock = eval(read)

    print(f"<<<当前 <str_ditc.txt> 中的内容:>>>\n"
          f"代码={stocks['code']}\n"
          f"名称={stock['name']}\n"
          f"价格={stock['price']}\n"
          f"增减={stock['change']}\n"
          )

    while True:
        user_choose = input("输入要更改的数据的类型的代码\n"
                      "(1=代码 2=名称 3=价格 4=增减）\n"
                    ">>>")

        if user_choose == "break":
            print(f"<<<已将 <str_ditc.txt> 中的内容保存为:>>>\n"
                  f"代码={stock['code']}\n"
                  f"名称={stock['name']}\n"
                  f"价格={stock['price']}\n"
                  f"增减={stock['change']}\n"
                  )
            with open("str_ditc.txt", mode="w", encoding="utf-8") as f:
                f.write(str(stock))
                exit()

        elif user_choose == "1":
            user_input = input("输入要更改为的数值\n>>>")
            stock["code"] = user_input
            break

        elif user_choose == "2":
            user_input = input("输入要更改为的数值\n>>>")
            stock["name"] = user_input
            break

        elif user_choose == "3":
            user_input = input("输入要更改为的数值\n>>>")
            stock["price"] = user_input
            break

        elif user_choose == "4":
            user_input = input("输入要更改为的数值\n>>>")
            stock["change"] = user_input
            break

        else:
            print(f"输入的 <{user_choose}> 非法，输入1~4的数字")

    with open("str_ditc.txt", mode="w", encoding="utf-8") as f:
        f.write(str(stock))

    print(f"修改后 <str_ditc.txt> 中的内容=\n"
          f"代码={stock['code']}\n"
          f"名称={stock['name']}\n"
          f"价格={stock['price']}\n"
          f"增减={stock['change']}\n"
          )



