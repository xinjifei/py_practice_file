''''
创建一个列表 scores，初始成绩：76, 92, 85, 64
打印欢迎语：欢迎使用成绩管理系统
显示菜单（让用户选择操作）：
plaintext
请选择功能：
1. 查看所有成绩
2. 添加新成绩
3. 修改成绩
4. 删除成绩
5. 查看成绩总数并退出
功能 1：输入 1 → 遍历打印所有成绩
功能 2：输入 2 → 输入新成绩，添加到列表末尾
功能 3：输入 3 → 输入要修改的第几个成绩，再输入新成绩进行修改
功能 4：输入 4 → 输入要删除的第几个成绩，执行删除
功能 5：输入 5 → 打印成绩总数，然后程序结束
除了 1-5 以外的输入 → 提示：输入错误，请重新选择
程序要一直运行，直到用户选择 5 才退出
'''

scores = [76, 92, 85, 64]

print('欢迎使用成绩管理系统')
print('请选择功能：\n1. 查看所有成绩\n2. 添加新成绩\n3. 修改成绩\n4. 删除成绩\n5. 查看成绩总数并退出\n（输入数字使用对应功能）')

while True:

    user_choose = input('<<<根目录>>>\n请选择功能（输入数字使用对应功能）\n请输入文本：')

#查看所有成绩
    if user_choose == '1':
        print('选择了功能1')

        print(f'所有成绩：\n{scores}')

#添加新成绩
    elif user_choose == '2':
        print('选择了功能2')

        new_scores = int(input('输入要添加的成绩（如果要退出该功能输入数字 -1）：'))

        if new_scores == -1:
            print('已退出功能2')

        else:
            scores.append(new_scores)
            print(f'成功将<{new_scores}>添加到了列表的最后一位，更改后的列表：\n{scores}')

#修改成绩
    elif user_choose == '3':
        print('选择了功能3')

        print(f'当前列表{scores}')
        replace = int(input('输入要更换的成绩所在列表中的位数（如果要退出该功能输入数字 -1）：'))

        if replace == -1:
            print('已退出功能3')

        else:
            replace = replace - 1
            replace_value = int(input(f'输入列表中第<{replace}>位将要被替换的新数值'))
            scores[replace] = replace_value
            print(f'成功将处在列表第<{replace}>位的成绩替换为{replace_value}，更改后的列表：\n{scores}')

#删除成绩
    elif user_choose == '4':
        print('选择了功能4')

        _del = int(input('输入要删除的成绩所在列表中的位数（如果要退出该功能输入数字 -1）：'))

        if _del == -1:
            print('已退出功能4')

        else:
            _del = _del - 1
            del scores[_del]
            print(f'成功将处在第{_del}位上的数字删除了，更改后的列表：\n{scores}')



#查看成绩总数并退出
    elif user_choose == '5':
        print('选择了功能5')
        print(scores)
        break

    else:
        print(f'输入的<{user_choose}>非法，输入1~5之间的数字用以选择功能')

print('<<<已退出>>>')