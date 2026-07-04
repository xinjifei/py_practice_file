#转换变量值类型使用格式{需要转换的格式（变量名）}

#例
#目的：将两个字符串类型数据相加后输出整形数据
#赋值变量name1、name2
name1='1'
name2='2'

#转换类型（str—>int)
name1_1=int(name1)
name2_1=int(name2)

#相加
jieguo=name1_1+name2_1
print(f'jieguo={jieguo},type(jieguo)={type(jieguo)}')

#两个字符串类型变量相加=将两个数据拼接
#例
name3='1'
name4='2'
jieguo2=name3+name4
print(f'jieguo2={jieguo2},type(jieguo2)={type(jieguo2)}')
