'''
练习题：学生成绩小管理（检验你完全掌握列表）
难度和你第一个登录练习完全一致
只用到列表基础操作：创建、添加、删除、修改、查询、遍历
题目要求
    创建一个列表，存储 3 个学生的成绩：85, 92, 78
    打印出整个成绩列表
    添加一个新成绩：90 到列表末尾
    修改第 2 个成绩为 95
    删除第 1 个成绩
    遍历列表，打印出每一个成绩
    最后打印出列表里一共有多少个成绩
'''

results = [85,92,78]

print(results)

results.append(90)

results[2] = 95

del results[1]

for score in results:
    print(score)

list_quantity = len(results)
print(f'列表中有{list_quantity}个成绩')