from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.runnables import RunnableLambda

model = ChatTongyi(model='qwen3-max')
str_parser = StrOutputParser()

first_prompt = PromptTemplate.from_template(
    '我的邻居姓{lastname}, 生了一个{gender}, 帮他起一个名字。仅回复名字')

second_prompt = PromptTemplate.from_template('解释{name}的含义')

my_func = RunnableLambda(lambda ai_msg: {'name': ai_msg.content})

# chain = first_prompt | model | my_func
chain = first_prompt | model | my_func | second_prompt | model | str_parser

res = chain.invoke({'lastname': '马', 'gender': '女儿'})

print(res)