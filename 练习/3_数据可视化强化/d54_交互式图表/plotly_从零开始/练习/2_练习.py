import plotly.express as px #type:ignore
import pandas as pd

#dataframe
data = {
    "城市": ["北京", "上海", "广州", "成都", "拉萨"],
    "人均收入(万)": [8.91, 9.20, 8.06, 4.80, 4.00],
    "平均寿命(岁)": [82.9, 84.11, 82.6, 80.2, 72.5],
    "地区": ["华北", "华东", "华南", "西南", "西南"],
    "人口(万)": [2180, 2485.41, 1910.1, 2153.5, 88.3]
}
df = pd.DataFrame(data)
#print(df["城市"])

#转换数据
cities = df["城市"].tolist()
income = df["人均收入(万)"].tolist()
lifespan = df["平均寿命(岁)"].tolist()
region = df["地区"].tolist()
population = df["人口(万)"].tolist()

#配置画图
fig = px.scatter(
    x=income,
    y=lifespan,
    color=region,
    size=population,
    title="多维数据显示",
    hover_name=cities
)

#画图
fig.show()


