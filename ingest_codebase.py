import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document 
from langchain_text_splitters import RecursiveCharacterTextSplitter 

# Configuration
SOURCE_DIRECTORY = "./app" 
INDEX_PATH = "data/faiss_index"
ALLOWED_EXTENSIONS = {".py", ".md", ".txt", ".json"}

def load_documents(source_dir):
    documents = []
    print(f"📂 Scanning directory: {source_dir}...")
    
    if not os.path.exists(source_dir):
        print(f"❌ Error: Folder '{source_dir}' does not exist.")
        return []

    for root, _, files in os.walk(source_dir):
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in ALLOWED_EXTENSIONS:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    doc = Document(
                        page_content=content,
                        metadata={"source": file_path}
                    )
                    documents.append(doc)
                    print(f"   📄 Loaded: {file}")
                except Exception as e:
                    print(f"   ❌ Error reading {file}: {e}")
    
    return documents

def main():
    print("\n--- 1. Loading Project Files ---")
    docs = load_documents(SOURCE_DIRECTORY)
    
    if not docs:
        print("❌ No documents found. Make sure your code is inside the '/app' folder.")
        return

    print(f"\n--- 2. Splitting Text ({len(docs)} files) ---")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    chunks = text_splitter.split_documents(docs)
    print(f"✅ Created {len(chunks)} searchable chunks.")

    print("\n--- 3. Creating Embeddings (Local CPU) ---")
    
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    print("\n--- 4. Saving to FAISS Vector Database ---")
    
    os.makedirs("data", exist_ok=True)
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(INDEX_PATH)
    
    print(f"\n✅ SUCCESS! Knowledge base saved to '{INDEX_PATH}'.")
    print("🚀 You can now run: uvicorn app.main:app --reload")

if __name__ == "__main__":
    main()