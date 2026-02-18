from openai import OpenAI, Stream
import os

from openai.types.chat import ChatCompletion, ChatCompletionChunk

client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),  # OPENAI_API_KEY
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

messages = [
    {"role": "system", "content": "不说废话简单回答"},
    {"role": "assistant", "content": "我是你的助手。"},
    {"role": "user", "content": "你是谁"}]
completion: ChatCompletion | Stream[ChatCompletionChunk] = client.chat.completions.create(
    model="qwen3-max",  # 您可以按需更换为其它深度思考模型
    messages=messages,
    extra_body={"enable_thinking": True},
    stream=True
)

# 打印completion变量:
print(completion)

# 不使用stream流
# print(completion.choices[0].message.content)
# for chunk in completion:
#     print(chunk)


is_answering = False  # 是否进入回复阶段
print("\n" + "=" * 20 + "思考过程" + "=" * 20)
for chunk in completion:
    delta = chunk.choices[0].delta
    if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
        if not is_answering:
            print(delta.reasoning_content, end="", flush=True)
    if hasattr(delta, "content") and delta.content:
        if not is_answering:
            print("\n" + "=" * 20 + "完整回复" + "=" * 20)
            is_answering = True
        print(delta.content, end="", flush=True)
