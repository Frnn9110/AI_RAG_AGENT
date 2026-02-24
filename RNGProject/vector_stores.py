from langchain_chroma import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_community.embeddings import DashScopeEmbeddings

import config_data as config


class VectorService(object):
    def __init__(self, embedding):
        self.embedding = embedding
        self.vector = Chroma(collection_name=config.collection_name,
                             persist_directory=config.persist_directory,
                             embedding_function=self.embedding)

    def retriever(self):
        return self.vector.as_retriever(kwargs={'k': config.search_threshold})


if __name__ == '__main__':
    vector_service = VectorService(DashScopeEmbeddings(model='text-embedding-v4'))
    contexts = vector_service.retriever().invoke('我的身高是180cm，体重是73kg')
    for doc in contexts:
        print(doc.page_content)
