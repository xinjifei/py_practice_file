#del用于删除变量值+++
a =  1

print(a)

del a
#print(a) 会报错，因为变量名未赋值

#使用特定格式删除 列表 中的特定值+++
list = [1,2,3]
print(list,'（befor del）')

del list[1]#这里的 1 表示列表中的第二位值，因为第一位标记为 0 ，所以要想删除第一位就需要是 del list[0]
print(list,'（after del）')

#使用特定格式删除 字典 中的特定键+++
person = {"name":"steve", "age":25,"gender":"男"}

print(person,'（befor del）')

del person["gender"]

print(person,'（after del）')