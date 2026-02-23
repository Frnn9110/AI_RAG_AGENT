import json
import os
from typing import Sequence

from langchain_community.chat_models import ChatTongyi
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory


class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id, storage_path):
        self.storage_path = storage_path
        self.session_id = session_id

        self.file_path = os.path.join(self.storage_path, self.session_id)
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        all_messages = list(messages)
        all_messages.extend(messages)

        new_messages = [message_to_dict(new_message) for new_message in all_messages]
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(new_messages, f)

    @property
    def messages(self) -> list[BaseMessage]:
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                messages_data = json.load(f)
                return messages_from_dict(messages_data)
        except FileNotFoundError:
            return []

    def clear(self) -> None:
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump([], f)


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


def get_session(session_id):
    return FileChatMessageHistory(session_id, './_12_chat_history')


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

    # res = conversion_chain.invoke({'human_input': '小明有1只狗'}, config=session_config)
    # print(res)

    # res = conversion_chain.invoke({'human_input': '小红有3只猫'}, config=session_config)
    # print(res)

    res = conversion_chain.invoke({'human_input': '一共有几只动物'}, config=session_config)
    print(res)
