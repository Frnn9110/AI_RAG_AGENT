from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi

chat_template = ChatPromptTemplate.from_messages([
    ('system', '.....'),
    ('ai', '....'),
    MessagesPlaceholder('history_chat'),
    ('human', '.....')
])

history = [
    ('ai', '....'),
    ('human', '.....'),
    ('ai', '....'),
    ('human', '.....'),
]

# 非chain写法
# chat_message = chat_template.invoke({'history_chat': history})
#
# print(chat_message.to_string())
#
# model = ChatTongyi(model='qwen3-max')
# res = model.invoke(input=chat_message)
# 
# print(res)

# chain写法
model = ChatTongyi(model='qwen3-max')
chain = chat_template | model
res = chain.invoke({'history_chat': history})
print(res)