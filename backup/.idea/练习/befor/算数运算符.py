#算数运算符+ - * / //(整除，取整数) **幂运算

#例1（凤姐购物清单）
#输入单价
sydj=float(input('上衣单价是多少'))
kzdj=float(input('裤子单价是多少'))

#购买数量
sygs=int(input('凤姐买了几件上衣'))
kzgs=int(input('凤姐买了几件裤子'))

#折扣
zhekou=float(input('今天的折扣为(以小数表示）'))

#计算
jieguo_yj=zhekou*(sydj*sygs+kzdj*kzgs)
jieguo_yh=(sydj*sygs+kzdj*kzgs)-jieguo_yj

#输出
print(f'凤姐今天共花费{jieguo_yj:.2f}元')
print(f'共优惠了{jieguo_yh:.2f}元')

#拥有相同的变量名以及不同变量值的变量会取会取后面的值

#例1
a=10
a=20
print(f'a={a}')        #output=【a=20】









