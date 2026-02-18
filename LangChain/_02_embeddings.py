"""文本嵌入模型"""

from langchain_community.embeddings import DashScopeEmbeddings
import numpy as np

# 初始化嵌入模型对象，默认使用的是test-embedding-v1
embed = DashScopeEmbeddings()

a = embed.embed_query("我好喜欢你")
b = embed.embed_documents(["我喜欢你", "我稀饭你", "我稀罕你", "晚上吃什么"])


def cosine_similarity(vector_a, vector_b):
    return np.dot(vector_a, vector_b) / (np.linalg.norm(vector_a) * np.linalg.norm(vector_b))


print(cosine_similarity(a, a))
print(cosine_similarity(b[0], a))
print(cosine_similarity(b[0], b[1]))
print(cosine_similarity(b[0], b[2]))
print(cosine_similarity(b[0], b[3]))
