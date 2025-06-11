from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

import config
from manage_vectorstore import update_file_vectors


def process_document(file_name: str):

    file_type = file_name.split(".")[-1].lower()
    loader = get_loader(file_type)(config.WATCH_DIRECTORY + "/" + file_name)
    splitter = get_splitter(file_type)
    documents = loader.load()

    chunks = splitter.split_documents(documents)
    for chunk in chunks:
        chunk.metadata["filename"] = file_name

    return chunks


def get_loader(file_extension):
    """
    Get the appropriate document loader based on the file extension.
    """
    if file_extension == "txt":
        return TextLoader
    elif file_extension == "pdf":
        return PyPDFLoader
    else:
        raise ValueError(f"Unsupported file extension: {file_extension}")


def get_splitter(file_extension):
    """
    Get the appropriate text splitter based on the file extension.
    """
    if file_extension in ["txt", "pdf"]:
        return RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZES[file_extension],
            chunk_overlap=config.CHUNK_OVERLAPS[file_extension],
        )
    else:
        raise ValueError(f"Unsupported file extension for splitting: {file_extension}")
