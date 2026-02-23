ollama: ollama.com/search
cmd中: ollama run 模型名称     （运行模型）
ollama api调用: http://localhost:11434/v1

openai库基础：

    {"role": "assistant", "content": "我是你的助手。"},
    {"role": "user", "content": "你是谁"}

    message中的assistant相当于提交给ai的历史记录


LangChain:
    1、pip install langchain langchain-community langchain-ollama dashscope chromadb -i https://pypi.tuna.tsinghua.edu.cn/simple
        langchain:核心包
        langchain-community:社区支持包(千问模型需要这个包)
        langchain-ollama:Ollama支持包
        dashscope:阿里云通义千问的python SDK
        chromadb:轻量向量数据库


2、通义千问qwen-max是llms， qwen3-max是chat， 输出qwen-max用的是chunk, 输出qwen3-max用的是chunk.content
        for chunk in model.stream(input=message):
        print(chunk, end='', flush=True)
        print(chunk.content, end='', flush=True)

3、三类模型 llm、chat、text-embedding

4、FewShotPromptTemplate、PromptTemplate、ChatPromptTemplate中都有invoke和formate方法
    继承关系：
        ![img.png](img.png)
        ![img_1.png](img_1.png)
    区别：
        format： 
            字符串替换，得到的是string 
            .format(a=?,b=?)
            解析替换{}
        invoke： 
            Runnable得到的是PromptValue类对象  
            .invoke({'a':'?', 'b': '?'})
            解析替换{},解析MessagePlaceholder结构化占位符

5、chain链，将组件串联，上1个组件的输出作为下一个组件的输入，必须是Runnable接口的子类才能入链
    ![img_2.png](img_2.png)

6、jq库用法
    ![img_3.png](img_3.png)
    ![img_4.png](img_4.png)

7、pdf分割
    需安装pypdf (pip install pypdf)

