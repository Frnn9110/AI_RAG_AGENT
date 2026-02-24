from langchain_community.vectorstores import Chroma
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import TextLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 内置向量存储 InMemoryVectorStore & DashScopeEmbeddings
# docs = TextLoader(file_path='./data/Python基础语法.txt', encoding='utf-8').load()
#
# splitter = RecursiveCharacterTextSplitter(
#     chunk_size=500,
#     chunk_overlap=50
# )
#
# split_docs = splitter.split_documents(docs)
#
# vector_store = InMemoryVectorStore(embedding=DashScopeEmbeddings())
# vector_store.add_documents(documents=split_docs, ids=[f'id{id_name}' for id_name in range(0, 56)])
#
# similar_search = vector_store.similarity_search('迭代器是什么', 4)
# print(len(similar_search), similar_search)
# for doc in docs:
#     print(doc)
#
# vector_store.delete(ids=['id1'])


# 外部向量存储 Chroma & DashScopeEmbeddings

vector_chroma = Chroma(collection_name='test_01',
                       embedding_function=DashScopeEmbeddings(),
                       persist_directory='./chroma_langchain_db')  # 存储路径
docs = CSVLoader(file_path='./data/info.csv',
                 encoding='utf-8',
                 source_column='source').load()

vector_chroma.add_documents(documents=docs, ids=[f'id{i}' for i in range(1, len(docs) + 1)])

# vector_chroma.delete(ids=['id1'])

results = vector_chroma.similarity_search('python是不是很好学', 1, filter={'source': '黑马程序员'})
for res in results:
    print(res)

results = vector_chroma.similarity_search('能赚多少钱', 3)
for res in results:
    print(res)
