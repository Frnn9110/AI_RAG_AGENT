from langchain_community.llms.tongyi import Tongyi
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

llm_model = Tongyi(model='qwen-max')
chat_model = ChatTongyi(model='qwen3-max')

# 一次性输出
# res = model.invoke('你是谁？')
#
# print(res)


# 流式输出
# res = model.stream(input='你是谁')
#
# for chunk in res:
#     print(chunk, flush=True, end='')


# 使用HumanMessage
# message = [HumanMessage(content='你是谁')]
# res = model.stream(input=message)
# for chunk in res:
#     print(chunk, end='', flush=True)


# SystemMessage、AIMessage、HumanMessage
message = [SystemMessage(content='你是边塞一位诗人'),
           HumanMessage(content='帮我写一首唐诗'),
           AIMessage(content='锄禾日当午，汗滴禾下土，谁之盘中餐，粒粒皆辛苦'),
           HumanMessage(content='仿照上一首诗，在帮我写一首鹅鸦杀的')]
print('# llms：')
for chunk in llm_model.stream(input=message):
    print(chunk, end='', flush=True)


print('\nchat model：')
for chunk in chat_model.stream(input=message):
    print(chunk.content, end='', flush=True)

# model = Tongyi(model='qwen3-max')
# qwen3-max是一个chat模型
# 输出要用chunk.content
