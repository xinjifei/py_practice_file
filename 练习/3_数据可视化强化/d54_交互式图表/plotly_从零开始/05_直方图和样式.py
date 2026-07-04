"""
第五课：直方图（Histogram）+ 自定义样式
histogram 看数据的分布形态——集中在哪、偏左还是偏右、有没有双峰。
"""
import numpy as np
import plotly.express as px

# 生成 1000 个正态分布的随机数
np.random.seed(42)
scores = np.random.normal(loc=70, scale=15, size=1000)  # 均值70，标准差15

fig = px.histogram(
    x=scores,
    nbins=30,                          # 分成 30 个柱子
    title="成绩分布直方图",
    color_discrete_sequence=["#636EFA"],  # 柱子颜色
    opacity=0.8,                       # 透明度
)
# 加竖线标注均值和及格线
fig.add_vline(x=70, line_dash="dash", line_color="red",
              annotation_text="均值 70")
fig.add_vline(x=60, line_dash="dash", line_color="orange",
              annotation_text="及格线 60")

fig.update_layout(
    xaxis_title="分数",
    yaxis_title="人数",
    bargap=0.05,  # 柱子之间的间隙
)
fig.show()
