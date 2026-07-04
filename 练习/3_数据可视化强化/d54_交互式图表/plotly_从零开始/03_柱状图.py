"""
第三课：柱状图（Bar Chart）
和 scatter/line 用法完全一样，换一个函数名而已。
"""
import plotly.express as px

fruits = ["苹果", "香蕉", "橙子", "葡萄", "西瓜"]
sales = [23, 17, 35, 12, 29]

fig = px.bar(x=fruits, y=sales, title="水果销量")
fig.show()
