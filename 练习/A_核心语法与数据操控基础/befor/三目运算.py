#三分支结构if....else....的缩写
print('分值为100')

chengji=int(input('输入成绩'))

if chengji >= 80:
    print('成绩为优')
elif chengji >= 70:
    if chengji >= 70:
        print('成绩为良')
    else:
        print('成绩为中')
elif chengji >= 60:
    if chengji >= 60:
        print('成绩为中')
    else:
        print('成绩为差')
else:
    print('成绩为差')
