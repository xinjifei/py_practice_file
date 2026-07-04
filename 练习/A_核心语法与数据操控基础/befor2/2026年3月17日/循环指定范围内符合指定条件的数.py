#例：找出1~100之间的偶数

a = 0
while a < 100:

    #设置输出条件
    if a % 2 == 0:  #如果变量值除以2=0
        print('something',a)

    a += 1

print('循环执行结束')