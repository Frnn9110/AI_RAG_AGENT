md5_path = './md5_.text'
collection_name = 'rag'
persist_directory = './chroma_db'

chunk_size = 500
chunk_overlap = 50
separators = ["\n\n"]

max_split_char_number = 1000

search_threshold = 3
embedding_model_name = 'text-embedding-v4'
chat_model_name = 'qwen3-max'

session_config = {
    "configurable": {
        "session_id": "user_001",
    }
}
