import os
from app.core.llm_adapter import LLMAdapter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def terminal_test():
    print("\n--- 1. Initializing Embeddings ---")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    print("--- 2. Loading FAISS Index ---")
    index_path = "data/faiss_index"
    if not os.path.exists(index_path):
        print("Error: Index not found. Run ingest.py first.")
        return
        
    vectorstore = FAISS.load_local(
        index_path, 
        embeddings, 
        allow_dangerous_deserialization=True
    )
    
    print("--- 3. Searching for Context (RAG) ---")
    query = "When did the AI Co-Pilot project start?"
    docs = vectorstore.similarity_search(query, k=1)
    context = docs[0].page_content if docs else "No context found."
    print(f"Retrieved context: {context}")

    print("--- 4. Initializing TinyLlama (Loading RAM...) ---")
    llm = LLMAdapter()
    
    print("--- 5. Generating Answer (Final Step) ---")
    prompt = f"Context: {context}\nQuestion: {query}\nAnswer:"
    response = llm.generate_response(prompt, max_tokens=30)
    
    print("\n" + "="*30)
    print(f"AI RESPONSE: {response}")
    print("="*30 + "\n")

if __name__ == "__main__":
    terminal_test()

