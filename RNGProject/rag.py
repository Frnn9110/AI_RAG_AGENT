from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableWithMessageHistory
from file_history_store import get_history
from vector_stores import VectorService
import config_data as config
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings


def print_prompts(prompt):
    print(prompt.to_string())
    return prompt


class RagService(object):
    def __init__(self):
        self.vector_service = VectorService(DashScopeEmbeddings(model=config.embedding_model_name))
        self.retriever = self.vector_service.retriever()

        self.prompts = ChatPromptTemplate.from_messages([
            ('system', '请根据参考文档回答用户提问, 参考文档为：{context}'),
            ("system", "并且我提供用户的对话历史记录，如下："),
            MessagesPlaceholder("history"),
            ('human', '{input}')
        ])

        self.chat_model = ChatTongyi(model=config.chat_model_name)
        self.chain = self.__get_chain()

    def __get_chain(self):
        retriever = self.retriever

        def format_func(docs: list[Document]):
            if not docs:
                return '无相关参考资料'

            reference_str = ''
            for doc in docs:
                reference_str += f'文档片段:{doc.page_content}\n 文档元数据: {doc.metadata}\n\n'

            return reference_str

        # chain = {"input": RunnablePassthrough(),
        #          "context": self.retriever | format_func} | self.prompts | print_prompts | self.chat_model | StrOutputParser()

        def format_for_retriever(value: dict) -> str:
            return value["input"]

        def format_for_prompt_template(value):
            # {input, context, history}
            new_value = {}
            new_value["input"] = value["input"]["input"]
            new_value["context"] = value["context"]
            new_value["history"] = value["input"]["history"]
            return new_value

        chain = (
                {"input": RunnablePassthrough(),
                 "context": RunnableLambda(format_for_retriever) | retriever | format_func
                 } | RunnableLambda(format_for_prompt_template) | self.prompts | print_prompts |
                self.chat_model | StrOutputParser())
        conversation_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history",
        )

        return conversation_chain


if __name__ == '__main__':
    rag = RagService()
    res = rag.chain.invoke({'input': '推荐春季穿搭'}, config=config.session_config)
    print(res)
