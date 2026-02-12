import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

class RAGEngine:
    def __init__(self, index_path="data/faiss_index"):
        """
        Initializes the RAG Engine by loading the local FAISS index.
        """
        self.index_path = index_path
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        if os.path.exists(self.index_path):
            # allow_dangerous_deserialization is required for loading local pickles
            self.vectorstore = FAISS.load_local(
                self.index_path, 
                self.embeddings, 
                allow_dangerous_deserialization=True
            )
        else:
            raise FileNotFoundError(f"FAISS index not found at {self.index_path}")

    def search(self, query: str, k: int = 2):
        """
        Searches the vector database for the most relevant code chunks.
        """
        try:
            docs = self.vectorstore.similarity_search(query, k=k)
            if not docs:
                return "No relevant context found."
            
            # Combine retrieved chunks into a single context string
            context = "\n---\n".join([doc.page_content for doc in docs])
            return context
        except Exception as e:
            return f"Error during RAG search: {str(e)}"