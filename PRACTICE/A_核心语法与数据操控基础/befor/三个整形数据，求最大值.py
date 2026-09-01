a=int(input('a='))
b=int(input('b='))
c=int(input('c='))

if a != b and b != c and c != b and c != a:
    if a>b and a>c:
        print('最大值为a')
    elif b >a and b>c:
        print('最大值为b')
    else:
        print('最大值为c')

else:
    print('数值不得相同')

