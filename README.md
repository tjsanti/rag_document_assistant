# RAG Personal Assistant

A document-based personal assistant that uses Retrieval-Augmented Generation (RAG) to answer questions from your documents. Built with LangChain, ChromaDB, and OpenAI.

## Features

- **Document Processing**: Automatically processes PDFs and text files from a watched directory
- **Vector Store Management**: Maintains a persistent ChromaDB vector store that syncs with your documents
- **Conversational Memory**: Remembers context within each session
- **Smart Updates**: Only processes new or modified documents

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your OpenAI API key in a `.env` file:
```
OPENAI_API_KEY=your_api_key_here
```

3. Create a documents directory and add your files:
```bash
mkdir documents
```

## Usage

Run the assistant:
```bash
python main.py
```

The system will:
- Create a `documents` directory if it doesn't exist
- Process any new documents and update the vector store
- Start an interactive chat session

Add documents to the `documents/` folder and restart to include them in the knowledge base.

## Supported File Types

- `.txt` - Plain text files
- `.pdf` - PDF documents

## Project Structure

```
rag_assistant/
├── main.py              # Entry point
├── assistant.py         # Main assistant class
├── document_sync.py     # Directory monitoring
├── document_processor.py # Document processing
├── manage_vectorstore.py # Vector store operations
├── config.py           # Configuration settings
└── documents/          # Your documents go here
```

## Configuration

Edit `config.py` to customize:
- Document directory path
- Vector store location
- Chunk sizes and overlaps
- AI models used