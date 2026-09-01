#1
name='steve'
print(f'我的名字叫{name}请多多关照')

#2
name='steve'
nianling=18
print(f'我的名字叫{name},今年{nianling}岁，请多多关照')

#3
xuehao=22
print('我的学号是%06d'%(xuehao))
#%06 意为6位整数，%（xuehao）定义占位符（%06）

#4
danjia=9.00
goumai=5.00
huafei=danjia*goumai
print('单价为%.0f元，购买了%.0f斤，花费%.2f元'%(danjia,goumai,huafei))
#danjia*goumai=浮点变量值互乘;%.0f=保留该浮点型变量值0位小数;%f=浮点型变量值占位符

#5
xiaoshu=10.00  #代表百分数
print('共占比%.2f%%'%(xiaoshu))

#%d、%f、%s，分别为 整形占位符、浮点占位符、字符串占位符
#例
zhengxing=1
fudian=0.1
zifuchuan='zifuchuan1'
print('%d,%.1f,%s'%(zhengxing,fudian,zifuchuan))

#整形变量值占位符如果需要固定位数，则需使用{%0【需要的位数】d}的格式书写
#例
zhengxing=1
print(f'我的学号是%06d'%(zhengxing))

#%是python中的特殊符号，若想输出%这个符号，则需要输入%%
#例
bianliangzhi1=1
print(f'%d%%1'%(bianliangzhi1))

