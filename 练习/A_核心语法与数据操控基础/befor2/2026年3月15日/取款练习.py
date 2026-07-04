
qvkuan=input('是否进行取款操作（y/n）')
yve=int(100000)

#取款操作
if qvkuan == 'y':
    qvkuanjine=int(input('输入提款金额'))
    if qvkuanjine <= yve:
        print(f'突出钞票{qvkuanjine}(元）')
    else:
        print('余额不足')

else:
    print('进行其他操作。。。')



#退卡操作
xuanze=input('是否退卡（y/n）')

if xuanze == 'y':
    print('退卡成功')
else:
    print('其他操作。。。')





