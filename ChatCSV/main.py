from langchain.prompts import PromptTemplate
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms.ctransformers import CTransformers
from langchain_community.vectorstores import FAISS
from constants import csv_db
from interface import ChatQueryInterface


class ChatCSV(ChatQueryInterface):

    def __init__(self):
        self.model_type = "llama"
        self.model_path = "C:/models/llama-2-7b-chat.ggmlv3.q4_0.bin"
        self.embeddings_model_path = "sentence-transformers/all-mpnet-base-v2"

    def load_llm(self):
        """Load the LLM using the CTransformers library."""
        return CTransformers(
            model=self.model_path,
            model_type=self.model_type,
            max_new_tokens=256,
            context_length=512
        )

    def query_chat(self, query: str):
        """Process the query and return the result."""
        embeddings = HuggingFaceEmbeddings(model_name=self.embeddings_model_path, model_kwargs={"device": "cpu"})
        db = FAISS.load_local(csv_db, embeddings, allow_dangerous_deserialization=True)

        llm = self.load_llm()
        retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})
        
        qa_template = """
        Answer questions based on the CSV data. Make sure to answer the question based on the context provided.
        Question: {question}
        Context: {context}
        """
        qa = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            combine_docs_chain_kwargs={"prompt": PromptTemplate(template=qa_template, input_variables=["question", "context"])}
        )

        chat_history = []
        if not query.strip():
            return {"answer": "No query provided. Please ask a question."}

        result = qa({"question": query, "chat_history": chat_history})
        print(result)
        return result.get("answer", "No answer found.")

ChatCSV().query_chat(query="Please provide the lastname of Gilberto?")