#1当 while 行判断为 false
#例：

a = 0
while a < 10:
    print(a)
    a += 1

#2当循环体中执行到 break
#例：一个数除以2余1，除以3余1，除以4余1，找出这个数字

b = 2
while True:

    #设置条件
    if b % 2 == 1 and  b %  3 == 1 and b % 4 == 1:
        print(f'这个数字为{b}')
        break

    #设置增量
    b += 1
