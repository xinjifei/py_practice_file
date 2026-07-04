a=(input('a='))
b=(input('b='))
c=(input('c='))
if a==b and b==c:
    print("数值不得相同")
else:
    print("最大值为",sorted(((a,"a"),(b,"b"),(c,"c")),key=lambda x:x[0])[2][1])