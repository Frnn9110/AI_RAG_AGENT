from langchain_core.prompts import PromptTemplate
from langchain_community.llms.tongyi import Tongyi

prompt_template = PromptTemplate.from_template("我的邻居姓{lastname}， 生了一个{gender}，帮他起一个名字, 简单回答")

model = Tongyi(model="qwen-max")

# 普通写法
prompt_text = prompt_template.format(lastname="马", gender="男孩")
print(model.invoke(input=prompt_text))

# 链写法
chain = prompt_template | model
res = chain.invoke(input={"lastname": "马", "gender": "男孩"})
print(res)

'''rag  mcp'''
