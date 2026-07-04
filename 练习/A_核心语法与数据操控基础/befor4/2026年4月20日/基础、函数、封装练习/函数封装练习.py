''''''

'''
新建：三个文件夹（两个文件输出，一个文件输出最终结果）
赋值：用于存放计算结果的空列表
写入：将两个列表分别存入文件夹

赋值：读取两个文件中的列表并分别赋值为 列表1 和 列表2

for 值1（列表1） 值2（列表2） in zip(列表1， 列表2)
    赋值：和 = 值1 + 值2
    添加：将 和 添加至 输出列表

写入：输出列表值写入结果存放文件

赋值：读取输出文件中的内容
打印：打印读取输出文件中的内容（列表）
    
    
    

'''

file_name1 = "test1.txt"
file_name2 = "test2.txt"
file_name3 = "test3.txt"

#模拟原始数据>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
list_1 = [1, 2, 3, 4, 5, 6]
list_2 = [1, 2, 3, 4, 5, 6]
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
list_3 = []

#写入
def write_file(file_name, input_value):
    with open(file_name,"w") as f:
        f.write(str(input_value))

write_file(file_name1, list_1)
write_file(file_name2, list_2)
write_file(file_name3, "")

#读取
def read_file(file_name):
    with open(file_name,"r") as f:
        output = f.read()
        return eval(output)

list1 = read_file(file_name1)
list2 = read_file(file_name2)

for a, b in zip(list1, list2):
    output = a + b
    list_3.append(output)

write_file(file_name3, list_3)

output_list = read_file(file_name3)

print(output_list)


















