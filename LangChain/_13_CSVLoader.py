from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(
    file_path='./data/stu.csv',
    encoding='utf-8',
    csv_args={
        'delimiter': ',',
        'quotechar': "'",

        # 如果元数据有表头，指定field name会把第一行当作数据
        'fieldnames': ['a', 'b', 'c', 'd']
    }
)

#
# documents = loader.load()
# for document in documents:
#     print(document)


for document in loader.lazy_load():
    print(document)
