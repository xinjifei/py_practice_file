# -*- coding: utf-8 -*-
# demo_embedding.py —— Embedding 全流程参考脚手架（不是练习答案）
#
# 练习要求：股票「业务描述」→ 向量 → 余弦相似度 → 2D 图
# 本 demo 故意换成「动物/水果」的短词，让你看思路，再自己做练习数据。
#
# 安装依赖（首次运行前）：
#   uv add sentence-transformers scikit-learn
#
# 流程分 3 步，正好对应今天的三个核心概念：
#   ① 文字 → 向量（Embedding 的本质）
#   ② 向量距离 = 语义相似度（余弦相似度）
#   ③ 降到 2D 画出来（PCA 降维可视化）

import sys
sys.path.append("d:/math_practice_file/function")   # 让 demo 能 import 统一的 plot()
from plot import plot
import numpy as np

# ============ ① 文字 → 向量 ============
from sentence_transformers import SentenceTransformer

# SentenceTransformer("模型名")：加载一个预训练模型
#   参数 "paraphrase-multilingual-MiniLM-L12-v2" 是 HuggingFace 上的模型 id，
#   这个是多语言版，中文效果好；输出 384 维向量
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# 待嵌入的文字：demo 用动物/水果，练习请换成股票业务描述
texts = ["猫", "狗", "老虎", "苹果", "香蕉"]

# model.encode(文字列表)：一次把多句话变成向量
#   输入：list[str]（一句话一个元素）
#   输出：(n, 384) 的 numpy 矩阵，每一行就是那句话的向量
embeddings = model.encode(texts)
print("向量形状:", embeddings.shape)      # 期望 (5, 384)

# ============ ② 向量距离 = 语义相似度 ============
from sklearn.metrics.pairwise import cosine_similarity

# cosine_similarity(向量矩阵)：算「两两之间的余弦相似度」
#   输入：(n, d) 矩阵 → 输出：(n, n) 相似度矩阵
#   相似度[i, j] = 第 i 句和第 j 句的余弦相似度（夹角的余弦）
#   值范围 -1 ~ 1：越接近 1 表示方向越一致 → 语义越像
sim = cosine_similarity(embeddings)

np.set_printoptions(precision=2, suppress=True)   # 只显示 2 位小数，好读
print("相似度矩阵：\n", sim)
print("「猫」 vs 「狗」    :", sim[0, 1])   # 同为动物，期望接近 1
print("「猫」 vs 「苹果」  :", sim[0, 3])   # 动物 vs 水果，期望明显更低

# ============ ③ 降到 2D 画出来 ============
from sklearn.decomposition import PCA

# PCA(n_components=2)：把高维向量「压扁」到 2 维
#   参数 n_components=2 表示目标维度是 2（384 维画不出来，只能看主要差异方向）
pca = PCA(n_components=2)

# fit_transform(向量矩阵)：先「学习」主要差异方向，再把数据投到 2 维
#   输入：(n, 384) → 输出：(n, 2)
emb_2d = pca.fit_transform(embeddings)

# 用统一的 plot() 画点：point 层 data 是 (n,2) 矩阵，labels 是每个点的名字
plot(
    [{"type": "point", "data": emb_2d, "labels": texts}],
    title="文字 → 向量 → 2D 可视化（PCA 降维）",
)
