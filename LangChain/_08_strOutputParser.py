from langchain_core.messages import AIMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_community.llms.tongyi import Tongyi

parser = StrOutputParser()

prompt_template = PromptTemplate.from_template('我的邻居姓{lastname}, 生了一个{gender}, 帮我取一个名字')

model = ChatTongyi(model='qwen3-max')
# model = Tongyi(model='qwen3-max')

chain = prompt_template | model

res = chain.stream({"lastname": "张", "gender": "女儿"})


for chunk in res:
    print(res, end='', flush=True)
# print(type(res))

# print(parser.invoke(res), type(parser.invoke(res)))
