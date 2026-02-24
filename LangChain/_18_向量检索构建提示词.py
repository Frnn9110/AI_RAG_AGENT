from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import InMemoryVectorStore
from langchain_community.chat_models import ChatTongyi

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


chain = prompt | print_prompt | model | StrOutputParser()

input_text = '怎么减肥？'

references = vector.similarity_search(input_text, 3)
reference_content = '['
for reference in references:
    reference_content += reference.page_content
reference_content += ']'

res = chain.invoke({"context": reference_content, "input": input_text})
print(res)
