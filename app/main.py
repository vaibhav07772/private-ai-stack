from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.rag import get_rag_context
from core.inference import get_llm_response
from core.guardrails import check_safety

load_dotenv()

app = FastAPI(title="Private AI Stack", version="1.0.0")

class QueryRequest(BaseModel):
    query: str
    use_rag: bool = True

@app.post("/ask")
async def ask(request: QueryRequest):
    # 1. Safety Check
    if not check_safety(request.query):
        raise HTTPException(status_code=400, detail="Unsafe query detected")
    
    # 2. RAG (if enabled)
    context = ""
    if request.use_rag:
        context = get_rag_context(request.query)
    
    # 3. LLM Inference
    response = get_llm_response(request.query, context)
    
    return {"response": response, "rag_used": request.use_rag}

@app.get("/")
async def root():
    return {"message": "Private AI Stack is running! Use POST /ask"}