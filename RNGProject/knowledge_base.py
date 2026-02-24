"""
知识库
"""
import os
from datetime import datetime

# from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config
import hashlib
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma


def check_md5(md5_str: str):
    if not os.path.exists(config.md5_path):
        open(config.md5_path, 'w', encoding='utf-8').close()
        return False
    else:
        with open(config.md5_path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip()
                if line == md5_str:
                    return True
        return False


def save_md5(md5_str):
    with open(config.md5_path, 'a', encoding='utf-8') as f:
        f.write(md5_str + '\n')


def get_string_md5(input_str: str, encoding='utf-8'):
    str_byte = input_str.encode(encoding=encoding)
    md5_obj = hashlib.md5()
    md5_obj.update(str_byte)
    md5_hex = md5_obj.hexdigest()
    return md5_hex


class KnowledgeBaseService(object):
    def __init__(self):
        os.makedirs(config.persist_directory, exist_ok=True)

        self.spliter = RecursiveCharacterTextSplitter(chunk_size=config.chunk_size,
                                                      chunk_overlap=config.chunk_overlap,
                                                      separators=config.separators,
                                                      length_function=len)
        self.chroma = Chroma(collection_name=config.collection_name,
                             embedding_function=DashScopeEmbeddings(model='text-embedding-v4'),
                             persist_directory=config.persist_directory)

    def upload_by_str(self, data, filename):
        """对传入的字符串向量化"""
        str_md5 = get_string_md5(data)
        if check_md5(str_md5):
            return "[跳过]内容已存在知识库中"

        if len(data) > config.max_split_char_number:
            knowledge_chunk = self.spliter.split_text(data)
        else:
            knowledge_chunk = [data]

        metadata = {
            "source": filename,
            "crate_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'operator': '小王'
        }

        self.chroma.add_texts(knowledge_chunk,
                              metadatas=[metadata for _ in knowledge_chunk])
        save_md5(str_md5)

        return "[上传成功]"


if __name__ == '__main__':
    service = KnowledgeBaseService()
    r = service.upload_by_str('周杰伦', 'testfile')
    print(r)
