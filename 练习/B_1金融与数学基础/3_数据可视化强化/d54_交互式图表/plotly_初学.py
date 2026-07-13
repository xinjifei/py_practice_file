import random
import plotly.express as px

#赋值类
class Die:
    def __init__(self, sides_num=6):
        self.sides_num = sides_num
    def roll(self):
        side = random.randint(1, self.sides_num)
        return side

#生成骰子结果列表
die = Die()
results = []
for _ in range(1000):
    res = die.roll()
    results.append(res)

def test():
    cont = 0
    for i in results:
        print(i)
        cont += 1
        if cont == 10:
            break
#test()

#统计各个面数的出现次数
frequncies = []
poss_results = range(1, die.sides_num + 1)
for side in poss_results:
    frequncy = results.count(side)
    frequncies.append(frequncy)
print(frequncies)

# 画图
fig = px.bar(x=poss_results, y=frequncies)
fig.show()