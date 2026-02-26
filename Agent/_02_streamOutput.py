from langchain.agents import create_agent
from langchain_community.chat_models import ChatTongyi
from langchain_core.tools import tool


@tool(description='股票价格查询')
def get_price(name: str):
    return f'{name}价格为： 120000美元'


@tool(description='')
def get_info(name: str):
    return f"{name}是一家公司，由mwf于2009年创建，mwf概念由MA提出"


agent = create_agent(ChatTongyi(mode='qwen3-max'),
                     tools=[get_info, get_price],
                     system_prompt='你是一个智能助手，可以回答股票相关问题，请告知我思考过程，让我知道为什么调用某个工具', )

for chunk in agent.stream(input={'messages': [{'role': 'user', 'content': 'mwf当前价格多少, 介绍一下？'}]}, stream_mode='values'):
    last_message = chunk['messages'][-1]
    if last_message.content:
        print(type(last_message).__name__, last_message.content)

    try:
        if last_message.tool_calls:
            print(f"工具调用： {[tool['name'] for tool in last_message.tool_calls]}")
    except AttributeError as e:
        pass