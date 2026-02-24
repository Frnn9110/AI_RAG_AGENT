#  向量检索入链
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import InMemoryVectorStore
from langchain_community.chat_models import ChatTongyi
from langchain_core.runnables import RunnablePassthrough

vector = InMemoryVectorStore(embedding=DashScopeEmbeddings(model='text-embedding-v4'))
prompt = ChatPromptTemplate.from_messages([
    ('system', '请根据提供的参考信息回答问题，参考信息为：{context}'),
    ('human', '{input}')]

)

vector.add_texts(['减肥要多喝水。', '减肥要少吃碳水。', '减肥要多做有氧运动。', '跑步是很好的有氧运动。'])

model = ChatTongyi(model='qwen3-max')


def print_prompt(prompt):
    print(prompt.to_string())
    return prompt


def format_func(docs: list[Document]):
    if not docs:
        return "无相关参考资料"
    reference_content = '['
    for reference in docs:
        reference_content += reference.page_content
    reference_content += ']'

    return reference_content


retriever = vector.as_retriever(search_kwargs={"k": 3})

chain = (
        {"input": RunnablePassthrough(),
         "context": retriever | format_func} | prompt | print_prompt | model | StrOutputParser()
)

# references = vector.similarity_search(input_text, 3)

input_text = '怎么减肥？'
res = chain.invoke(input_text)
print(res)
