#水平制表符（类似4个空格）
print('1\t2')

#换行符
print('3\n4')

#反斜杠
print('\\')

#单引号
print('他说\'1\'')


#使用{end='【数值】'}来让控制台输出内容不换行
#例
print(1,end='\t')
print(2)

#输出格式补充
name1=1
name2=2
print(f'name1={0},name2={1}'.format(name1,name2))
