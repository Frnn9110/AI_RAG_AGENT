from langchain_community.document_loaders import JSONLoader

# loader = JSONLoader(
#     file_path='./data/stu.json',
#     jq_schema='.',
#     text_content=False,
# )
# document = loader.load()
# print(type(document), document)


# loader = JSONLoader(
#     file_path='./data/stus.json',
#     jq_schema='.[].name',
#     text_content=True,
# )
# document = loader.load()
# print(type(document), document)


loader = JSONLoader(
    file_path='./data/stu_json_lines.json',
    jq_schema='.name',
    text_content=False,
    json_lines=True
)
documents = loader.load()
for document in documents:
    print(type(document), document.page_content)
