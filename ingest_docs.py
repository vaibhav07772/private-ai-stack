# ingest_docs.py — Run this once to add all your documents to the vector DB
from core.rag import create_vectorstore
import os

if __name__ == "__main__":
    docs_path = "./data/docs"
    
    # Create folder if missing
    if not os.path.exists(docs_path):
        os.makedirs(docs_path)
        print(f"📁 Created folder: {docs_path}")
        print("⚠️ Please add some PDF or TXT files to this folder and run again.")
        exit()
    
    # Check if files exist
    files = os.listdir(docs_path)
    if not files:
        print(f"⚠️ No files found in {docs_path}. Please add PDF/TXT files.")
        print("💡 Tip: Copy your sample files from the earlier project (faculty_sample.txt, fee_sample.txt, etc.)")
        exit()
    
    print(f"📄 Found {len(files)} files in {docs_path}:")
    for f in files:
        print(f"   - {f}")
    
    print("\n🔄 Starting ingestion into ChromaDB...")
    result = create_vectorstore(docs_path)
    
    if result:
        print("\n✅ Ingestion complete! Now go to Streamlit and query with RAG ON.")
    else:
        print("\n❌ Ingestion failed. Check the errors above.")