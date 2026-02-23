from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loder = TextLoader(file_path='./data/Python基础语法.txt', encoding='utf-8')
docs = loder.load()
print(docs)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # 分段最大字符数
    chunk_overlap=50,  # 分段之间允许重复字符数
    separators=['!', '?', '.', '\n', '\n\n', '？', '。', '！', ' ', ''],
    length_function=len
)

split_docs = splitter.split_documents(docs)
for doc in split_docs:
    print('='*20)
    print(doc)
