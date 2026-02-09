import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def run_ingestion():
    data_path = "data/"
    if not os.path.exists(data_path):
        os.makedirs(data_path)
        
    documents = []
    
    for file in os.listdir(data_path):
        file_path = os.path.join(data_path, file)
        if file.endswith(".txt"):
            documents.extend(TextLoader(file_path).load())
        elif file.endswith(".pdf"):
            documents.extend(PyPDFLoader(file_path).load())

    if not documents:
        print("No documents found in /data folder.")
        return

    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = splitter.split_documents(documents)
    
    # Using a free, local model for embeddings (no API key needed)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local("data/faiss_index")
    print("Ingestion complete. Index saved to data/faiss_index")

if __name__ == "__main__":
    run_ingestion()