import os
from typing import List

from langchain_chroma.vectorstores import Chroma
from langchain_openai.embeddings import OpenAIEmbeddings

import config


def load_vectorstore():
    """
    Load the Chroma vector store from the specified data directory.
    If it doesn't exist, create a new one.
    """
    if not os.path.exists(config.VECTORSTORE_PATH):
        print(
            "I see this is your first time running the RAG assistant. "
            "I will create a new vector store for you."
        )
        return create_vectorstore()

    try:
        vectorstore = Chroma(
            collection_name=config.COLLECTION_NAME,
            persist_directory=config.VECTORSTORE_PATH,
            embedding_function=OpenAIEmbeddings(model=config.EMBEDDING_MODEL),
        )

        return vectorstore
    except Exception as e:
        print(f"Error loading vector store: {e}")
        raise RuntimeError(
            f"Failed to load vector store from {config.VECTORSTORE_PATH}. "
            "Please ensure the path is correct and the vector store is initialized."
        )


def create_vectorstore():

    return Chroma(
        collection_name=config.COLLECTION_NAME,
        persist_directory=config.VECTORSTORE_PATH,
        embedding_function=OpenAIEmbeddings(model=config.EMBEDDING_MODEL),
    )


def update_file_vectors(vector_store, filename: str, new_chunks: List[str]):
    # Remove old vectors
    remove_file_vectors(vector_store, filename)

    # Add new vectors
    vector_store.add_documents(
        documents=new_chunks,
        ids=[f"{filename}_chunk_{i}" for i in range(len(new_chunks))],
    )


def remove_file_vectors(vector_store, filename: str):
    results = vector_store.get(where={"filename": filename})
    if results["ids"]:
        vector_store.delete(ids=results["ids"])
