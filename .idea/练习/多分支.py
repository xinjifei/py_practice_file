#elif

#根据学生的成绩划分等级

chengji=80

if chengji >= 80:
    print('成绩为优')
elif chengji >= 70:
    print('成绩为良')
elif chengji >= 60:
    print('成绩为中')
else:
    print('成绩为差')

'''
if chengji >= 80:
    print('成绩为优')
elif chengji >= 70:
    print('成绩为良')
elif chengji >= 60:
    print('成绩为中')
    

如果第一个判断生效则不会继续执行elif，若是无效则继续判断下一个。以此类推
总结：elif格式会在上一个条件不成立的条件下成立并执行

'''

#例
#判断语数英三科是否全部合格

ywcj=int(input('语文成绩'))
sxcj=int(input('数学成绩'))
yycj=int(input('英语成绩'))

if ywcj >= 60 and ywcj >= 60 and yycj >= 60:
    print('全部及格')
else:
    print('没有全部及格')

#判断哪个学科的分数最高
if ywcj > sxcj:
    if ywcj > yycj:
        print('语文成绩最高')
    else:
        print('英语成绩最高')

elif ywcj < sxcj:
    if sxcj < yycj:
        print('英语成绩最好')
    else:
        print('数学成绩最好')
#if条件嵌套



