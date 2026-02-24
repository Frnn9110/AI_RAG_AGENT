from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from RNGProject.vector_stores import VectorService
import config_data as config
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings


class RagService(object):
    def __init__(self):
        self.vector_service = VectorService(DashScopeEmbeddings(model=config.embedding_model_name))
        self.retriever = self.vector_service.retriever()

        self.prompts = ChatPromptTemplate.from_messages([
            ('system', '请根据参考文档回答用户提问, 参考文档为：{context}'),
            ('human', '{input}')
        ])

        self.chat_model = ChatTongyi(model=config.chat_model_name)
        self.chain = self.__get_chain()

    def __get_chain(self):
        def print_prompts(prompt):
            print(prompt.to_string())
            return prompt

        def format_func(docs: list[Document]):
            if not docs:
                return '无相关参考资料'

            reference_str = ''
            for doc in docs:
                reference_str += f'文档片段:{doc.page_content}\n 文档元数据: {doc.metadata}\n\n'

            return reference_str

        chain = {"input": RunnablePassthrough(),
                 "context": self.retriever | format_func} | self.prompts | print_prompts | self.chat_model | StrOutputParser()

        return chain


if __name__ == '__main__':
    rag = RagService()
    res = rag.chain.invoke('我体重140斤， 尺码推荐')
    print(res)
