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

chat_message = chat_template.invoke({'history_chat': history})

print(chat_message.to_string())

model = ChatTongyi(model='qwen3-max')
res = model.invoke(input=chat_message)

print(res)