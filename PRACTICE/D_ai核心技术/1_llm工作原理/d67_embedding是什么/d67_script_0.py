import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA

import sys
sys.path.append("D:/math_practice_file/function")
from plot_3d import plot_3d

model_id = "paraphrase-multilingual-MiniLM-L12-v2"
model = SentenceTransformer(model_id)

text = company_desc = [
    "宁德时代：动力电池与储能电池研发生产，布局换电及新能源应用方案",
    "京东方：半导体显示器件研发制造，供应LCD、OLED各类屏幕产品",
    "中国神华：煤炭开采销售，配套电力、铁路港口一体化能源业务",
    "比亚迪：新能源整车、动力电池研发制造，覆盖乘用车商用车领域",
    "同花顺：金融信息服务，证券行情软件、数据终端与智能投顾业务",
    "药明康德：医药研发外包服务，提供药物临床及生产一体化支持",
    "立讯精密：消费电子精密组件制造，代工组装多类智能硬件产品",
    "海天味业：调味品研发生产销售，主营酱油、蚝油等餐饮调味品",
    "金山办公：办公软件研发，WPS文档产品及云服务授权运营业务",
    "阳光电源：光伏逆变器、储能设备研发，提供新能源发电系统方案",
    "爱尔眼科：眼科医疗服务，开展屈光、眼底、视光等诊疗项目",
    "恒瑞医药：创新药研发生产销售，聚焦肿瘤、慢病等治疗领域"
]
labels = [
    "宁德时代",
    "京东方",
    "中国神华",
    "比亚迪",
    "同花顺",
    "药明康德",
    "立讯精密",
    "海天味业",
    "金山办公",
    "阳光电源",
    "爱尔眼科",
    "恒瑞医药"
]

embeddings = model.encode(text)
print(embeddings.shape)

sim = cosine_similarity(embeddings)
print(sim)
print("语义相似度矩阵（余弦相似度）")
print("embedding model = " ,model_id)

# —— 找最相似 / 最不相似的一对（排除对角线）——
s_max = sim.copy()
np.fill_diagonal(s_max, -1)
i, j = np.unravel_index(np.argmax(s_max), sim.shape)
print("最相似:", labels[i], "↔", labels[j], "相似度 =", round(sim[i, j], 4))

s_min = sim.copy()
np.fill_diagonal(s_min, 2)
i, j = np.unravel_index(np.argmin(s_min), sim.shape)
print("最不相似:", labels[i], "↔", labels[j], "相似度 =", round(sim[i, j], 4))

print("PCA降维开始")

pca = PCA(n_components=3)
pca_point = pca.fit_transform(embeddings)

print(pca_point.shape)

print("主成分方差解释率比例",pca.explained_variance_ratio_)
print("PCA result (componnenrs=3) = ", pca_point)

plot_3d([
    {"type":"point","data":pca_point,"labels":labels}
])


