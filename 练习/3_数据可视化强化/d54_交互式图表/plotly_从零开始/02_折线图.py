"""
第二课：折线图（Line Plot）
把 scatter 换成 line，点之间就连上线了。
"""
import plotly.express as px

x = [1, 2, 3, 4, 5]
y = [3, 7, 2, 8, 5]

fig = px.line(x=x, y=y, title="折线图 — 点被线连起来了")
fig.show()
