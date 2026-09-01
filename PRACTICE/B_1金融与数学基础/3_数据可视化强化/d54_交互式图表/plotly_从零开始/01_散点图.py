"""
入门第一课：散点图（Scatter Plot）
Plotly 最基础的用法 —— 告诉它 X 是什么、Y 是什么，它帮你画点。
"""
import plotly.express as px # pyright: ignore[reportMissingImports]

# 数据：就这么简单 —— 两个列表
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

# 一句话出图
fig = px.scatter(x=x, y=y, title="最简单的散点图")
fig.show()
