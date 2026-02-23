from openai import OpenAI, Stream

client = OpenAI(
    base_url='https://dashscope.aliyuncs.com/compatible-mode/v1',
    # api_key=os.getenv('DASHSCOPE_API_KEY')
)

client