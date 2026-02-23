from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi

json_parser = JsonOutputParser()
str_parser = StrOutputParser()

model = ChatTongyi(model='qwen3-max')

first_prompt = PromptTemplate.from_template(
    '我的邻居姓{lastname}, 生了一个{gender}, 帮他起一个名字。回复json格式, key为name, value为姓名')

second_prompt = PromptTemplate.from_template('解释{name}的含义')

chain = first_prompt | model | json_parser | second_prompt | model | str_parser

res = chain.stream({'lastname': '张', 'gender': '女儿'})

for chunk in res:
    print(chunk, end='', flush=True)
print(type(res))
