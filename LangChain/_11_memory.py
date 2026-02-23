from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

str_parser = StrOutputParser()
model = ChatTongyi(model='qwen3-max')

prompts = ChatPromptTemplate.from_messages(
    [
        ('system', '根据历史对话记录回复用户提问'),
        MessagesPlaceholder('history_message'),
        ('human', '用户提问：{human_input}')
    ],

)


def print_prompts(prompts):
    print(str(prompts))
    return prompts


base_chain = prompts | print_prompts | model | str_parser

session = {}


def get_session(session_id):
    if session_id not in session:
        session[session_id] = InMemoryChatMessageHistory()

    return session[session_id]


conversion_chain = RunnableWithMessageHistory(
    runnable=base_chain,
    get_session_history=get_session,
    input_messages_key='human_input',
    history_messages_key='history_message'
)

if __name__ == '__main__':
    session_config = {
        'configurable': {
            'session_id': 'user_001'
        }
    }

    res = conversion_chain.invoke({'human_input': '小明有1只狗'}, config=session_config)
    print(res)

    res = conversion_chain.invoke({'human_input': '小红有3只猫'}, config=session_config)
    print(res)

    res = conversion_chain.invoke({'human_input': '一共有几只动物'}, config=session_config)
    print(res)
