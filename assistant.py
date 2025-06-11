from langchain_openai.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

import config
from manage_vectorstore import load_vectorstore
from document_sync import get_files_needing_processing, mark_file_processed
from document_processor import process_document, update_file_vectors


class Assistant:

    def __init__(self):
        print("Hi! I'm your Document Assistant.")

        self.vectorstore = load_vectorstore()
        self._update_vectorstore()
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})

        self.store = {}
        self._setup_chains()

        print("How can I help you today?")

    def _setup_chains(self):
        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Given a chat history and the latest user question "
                    "which might reference context in the chat history, "
                    "formulate a standalone question which can be understood "
                    "without the chat history. Do NOT answer the question, "
                    "just reformulate it if needed and otherwise return it as is.",
                ),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        qa_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful personal assistant that answers questions about a user's documents.\n\n"
                    "Answer the question based on the provided context.\n\n"
                    "If you don't know the answer, say 'I don't know'.\n\n"
                    "Context:\n{context}",
                ),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        llm = ChatOpenAI(model_name=config.CHAT_MODEL, temperature=0.0)

        history_aware_retriever = create_history_aware_retriever(
            llm, self.retriever, contextualize_q_prompt
        )

        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

        rag_chain = create_retrieval_chain(
            history_aware_retriever, question_answer_chain
        )

        self.conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )

    def get_session_history(self, session_id: str):
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
        return self.store[session_id]

    def _update_vectorstore(self):

        files_to_process = get_files_needing_processing()
        if files_to_process is None:
            exit(
                "The document directory did not exist, so I created it for you.",
                " Make sure to add your documents there before trying again.",
                "Goodbye!",
            )
        elif len(files_to_process) == 0:
            return

        # Process each file and update the vector store
        print(
            "I see there are new files to process. Let me update my knowledge base..."
        )
        for file_name in files_to_process:
            new_chunks = process_document(file_name)

            # Update the vector store with new chunks
            update_file_vectors(self.vectorstore, file_name, new_chunks)
            print(f"Processed {file_name}")

            mark_file_processed(file_name)

        print("Okay we're all set! My knowledge base is up to date.")

    def query(self, query: str):

        return self.retriever.invoke(query)

    def answer_question(self, question, session_id="default"):
        result = self.conversational_rag_chain.invoke(
            {"input": question}, config={"configurable": {"session_id": session_id}}
        )
        return result["answer"]

    def run(self):
        """
        Main method to run the assistant.
        """

        while True:
            user_input = input("\nYou: ")

            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break

            if not user_input.strip():
                print("Please enter a valid question.")
                continue

            # Process the user input and get a response
            response = self.answer_question(user_input)
            print(f"Assistant: {response}")
