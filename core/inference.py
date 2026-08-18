# core/inference.py — MOCK VERSION (Instant response, no download)
import os

def get_llm_response(query, context=""):
    """Instant mock response — no model download needed"""
    
    # Check if context is available (RAG mode)
    if context and len(context.strip()) > 10:
        return f"""📄 **RAG Context Retrieved!**

**Context snippet:** {context[:200]}...

**Your Query:** {query}

✅ **Mock Response (RAG Mode):** 
Aapki query ka jawab document mein available hai. 
• RAG: ✅ Working
• Guardrails: ✅ Active
• System: ✅ Perfect

🔹 **Aage kya karna hai?** 
Real model download complete hone par (ya fine-tuned model load karke) real LLM responses aayenge."""
    else:
        return f"""🤖 **Mock Response (Direct Mode)**

**Your Query:** {query}

✅ **Test Successful!** 
Aapka FastAPI server, Guardrails, aur Streamlit UI bilkul sahi kaam kar rahe hain.

🔹 **Next Steps:**
1. Model download complete hone par real responses milenge.
2. Ya Google Colab mein fine-tuned model train karke HuggingFace se load kar sakte ho.

✅ **System Status:** Online & Ready!"""