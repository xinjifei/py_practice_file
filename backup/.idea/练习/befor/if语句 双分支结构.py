分值 = int(input('请输入分值：'))
成绩 = int(input('输入成绩：'))

if 分值 >= 成绩 and 成绩 >= 0:
    if 成绩 / 分值 >= 0.6:
        print('及格了')
    else:
        print('没有及格')
else:
    print('成绩必须要小于等于分值并大于等于零')

