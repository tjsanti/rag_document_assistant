# Paths
WATCH_DIRECTORY = "./documents"
VECTORSTORE_PATH = "./chroma_db"

# API
EMBEDDING_MODEL = "text-embedding-ada-002"
CHAT_MODEL = "gpt-4.1-mini"

# Document processing
CHUNK_SIZES = {"txt": 1000, "pdf": 1500}
CHUNK_OVERLAPS = {"txt": 200, "pdf": 300}

# Chroma settings
COLLECTION_NAME = "rag_assistant"
