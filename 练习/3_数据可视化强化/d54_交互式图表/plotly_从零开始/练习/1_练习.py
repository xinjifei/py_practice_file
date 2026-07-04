"""
练习 1： 
画一张散点图。X = [1, 3, 5, 7, 9]，Y = [10, 25, 15, 35, 20]，标题"我的第一张散点图"。
练习 2：
画一张折线图。X = 星期一到星期日（["周一","周二",...,"周日"]），Y = [15, 18, 12, 22, 19, 25, 28]（每天气温），标题"一周气温变化"。
练习 3： 
画一张柱状图。X = ["语文","数学","英语","物理","化学"]，Y = [88, 95, 72, 83, 91]，标题"期末成绩"。
"""
import plotly.express as px # type: ignore


#散点图
def fig_1(X:list, Y:list, title:str):
    fig = px.scatter(x=X, y=Y, title=title)
    fig.show()

#折线图
def fig_2(X:list, Y:list, title:str):
    fig = px.line(x=X, y=Y, title=title)
    fig.show()

#柱状图
def fig_3(X:list, Y:list, title:str):
    fig = px.bar(x=X, y=Y, title=title)
    fig.show()

if __name__ == "__main__":
    #散点图
    X = [1, 3, 5, 7, 9]
    Y = [10, 25, 15, 35, 20]
    #fig_1(X, Y, "第一个散点图")
    
    #折线图
    X = ["周一","周二","周三","周四","周五","周六","周日"]
    Y = [15, 18, 12, 22, 19, 25, 28]
    #fig_2(X, Y, "一周气温变化")

    #柱状图
    X = ["语文","数学","英语","物理","化学"]
    Y = [88, 95, 72, 83, 91]
    fig_3(X, Y, "期末成绩")



