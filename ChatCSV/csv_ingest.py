import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from constants import csv_db, file_path
from interface import ChatIngestInterface


class CSV_ingest(ChatIngestInterface):
    
    def __init__(self):
        self.embeddings_model = "sentence-transformers/all-mpnet-base-v2"

    def get_vectorstores(self):
        source_directory = os.path.join(os.getcwd(), file_path)
        for filename in os.listdir(source_directory):
            if filename.endswith(".csv"):
                file_paths = os.path.join(source_directory, filename)
                try:
                    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
                    loader = CSVLoader(file_path=file_paths)
                    data = loader.load()
                    documents = text_splitter.split_documents(data)
                    embeddings = HuggingFaceEmbeddings(model_name=self.embeddings_model)
                    db = FAISS.from_documents(documents, embeddings)
                    db.save_local(csv_db)
                    # os.remove(file_paths)
                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")
        return ("FaissDB Successfully created. Now you can run Query !!!")    
CSV_ingest().get_vectorstores()