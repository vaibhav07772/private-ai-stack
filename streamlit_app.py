import streamlit as st
import requests
import json

st.set_page_config(page_title="Private AI Stack", page_icon="🔒", layout="wide")

st.title("🔒 Private AI Stack")
st.markdown("*Fine-tuned Llama-3 + RAG + Guardrails*")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    api_url = st.text_input("API URL", value="http://localhost:8000/ask")
    use_rag = st.checkbox("Use RAG (Document Search)", value=True)
    st.markdown("---")
    st.markdown("**Safety Features Active:**")
    st.markdown("✅ PII Detection")
    st.markdown("✅ Jailbreak Prevention")
    st.markdown("✅ Toxicity Filter")

# Main Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Call API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                payload = {"query": prompt, "use_rag": use_rag}
                response = requests.post(api_url, json=payload, timeout=60)
                
                if response.status_code == 200:
                    data = response.json()
                    reply = data["response"]
                    if data.get("rag_used"):
                        st.caption("📄 Retrieved context from documents")
                    st.markdown(reply)
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
                    reply = f"⚠️ Error: {response.status_code}"
                    
            except Exception as e:
                st.error(f"Connection Error: {e}")
                reply = "⚠️ Could not connect to FastAPI server. Make sure it's running."
        
        st.session_state.messages.append({"role": "assistant", "content": reply})