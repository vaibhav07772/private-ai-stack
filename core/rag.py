import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

PERSIST_DIR = "./data/chroma_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

def get_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

def clean_text(text):
    """Remove null bytes and fix encoding artifacts"""
    # Remove null bytes (\x00)
    text = text.replace('\x00', '')
    # Remove UTF-16 BOM if present
    if text.startswith('\ufeff'):
        text = text[1:]
    return text

def load_text_with_fallback(filepath):
    """Try UTF-8, UTF-16, cp1252, then latin-1"""
    encodings = ['utf-8-sig', 'utf-16', 'cp1252', 'latin-1']
    for enc in encodings:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                content = f.read()
            # Clean the content
            content = clean_text(content)
            return content
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise UnicodeDecodeError(f"Could not decode {filepath} with any encoding")

def create_vectorstore(docs_path="./data/docs"):
    """PDF aur TXT files ko ChromaDB mein store karo"""
    documents = []
    
    if not os.path.exists(docs_path):
        os.makedirs(docs_path)
        print(f"📁 Created folder: {docs_path}. Please add some PDF/TXT files.")
        return None
    
    for file in os.listdir(docs_path):
        path = os.path.join(docs_path, file)
        try:
            if file.endswith('.pdf'):
                loader = PyPDFLoader(path)
                docs = loader.load()
                documents.extend(docs)
                print(f"✅ Loaded PDF: {file}")
            elif file.endswith('.txt'):
                content = load_text_with_fallback(path)
                doc = Document(page_content=content, metadata={"source": file})
                documents.append(doc)
                print(f"✅ Loaded TXT: {file}")
        except Exception as e:
            print(f"❌ Error loading {file}: {e}")
    
    if not documents:
        print("⚠️ No valid PDF/TXT files found in ./data/docs")
        return None
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)
    
    vectorstore = Chroma.from_documents(
        chunks,
        get_embeddings(),
        persist_directory=PERSIST_DIR
    )
    print(f"✅ Ingested {len(chunks)} chunks from {len(documents)} documents")
    return vectorstore

def get_rag_context(query, k=3):
    if not os.path.exists(PERSIST_DIR):
        return "No documents found. Please run ingestion first (python ingest_docs.py)."
    
    vectorstore = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=get_embeddings()
    )
    docs = vectorstore.similarity_search(query, k=k)
    if not docs:
        return "No relevant documents found for this query."
    
    # Clean context while returning
    context = "\n\n".join([doc.page_content for doc in docs])
    return clean_text(context)