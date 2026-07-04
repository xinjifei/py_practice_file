import csv

#场景一：文件不存在（[Errno 2] No such file or directory: 'file.csv'）
def read_csv(file_name):
    try:
        data = []
        with open(file_name, "r", encoding="utf-8") as f:
            csv_reader = csv.reader(f)
            next(csv_reader)

            for row in csv_reader:
                if not row:
                    continue
                data.append(row)

        print("✅ 文件读取成功！")
        return data

    except Exception as e:
        print(f"读取失败，原因={e}")
        return []

#read_csv("file.csv")

#场景二：除0错误(ZeroDivisionError: division by zero)
def  division():
    try:
        a = 20
        b = 0
        c = a / b
        print(c)
        return c

    except Exception as e:
        print(f"除数失败，原因={e}")

#division()

#场景三：下表越界（IndexError：list index out of range）
def subscript():
    try:
        list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        print(list[11])

    except Exception as e:
        print(f"取值失败，原因={e}")

#subscript()

#场景四：字符串转数字失败（ValueError）
def turn():
    try:
        num = float("something that made by str")
    except Exception as e:
        print(f"变量类型转换失败，原因={e}")





