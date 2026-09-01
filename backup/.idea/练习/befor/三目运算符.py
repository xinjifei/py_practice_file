a=int(input('a='))
b=int(input('b='))
c=int(input('c='))

if a != b and b != c and a !=c:
    dierda=a if a>b else b>a
    diyida=dierda if dierda > c else c
    print(f'第一大是{diyida}')
else:
    print('数值非法')


