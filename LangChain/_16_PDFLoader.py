# 需安装pypdf (pip install pypdf)

from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(
    file_path='./data/pdf2.pdf',
    mode='page',
    password='itheima'
)

docs = loader.lazy_load()
for i, doc in enumerate(docs, start=1):
    print('=' * 30)
    print(doc)
    print('=' * 30, i)
