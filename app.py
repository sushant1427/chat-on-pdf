import streamlit as st
from pdf_processing import context, Chunking
from gemini_api import response

st.set_page_config(page_title="Chatbot for pdf", page_icon="📄", layout="centered")
st.markdown("""
    <style>
        .upload-box {
            border: 2px dashed #ccc;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            color: #666;
        }
        .uploaded-file {
            font-size: 14px;
            margin-top: 10px;
            color: green;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📄 CHATBOT For PDF")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "document_chunks" not in st.session_state:
    st.session_state.document_chunks = []

# File upload box
st.markdown('<div class="upload-box">📂 Upload PDF<br><small>(Accept only PDF. Max size: 10MB)</small></div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type="pdf", label_visibility="collapsed")

if uploaded_file and not st.session_state.document_chunks:
    with st.spinner("Processing PDF..."):
        st.session_state.document_chunks = Chunking(uploaded_file)
        st.success(f"📄 {uploaded_file.name} — Pages: {len(st.session_state.document_chunks)} (processed successfully)")
        st.session_state.messages.append({
            "role": "assistant", "content": "✅ PDF uploaded successfully! You can now ask me questions about it."
        })

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if user_question := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            context = context(user_question, st.session_state.document_chunks)
            if context:
                prompt = f"""
                You are a helpful AI assistant. Answer based only on the document context.

                Context:
                {context}

                Question: {user_question}
                Answer:
                """
                try:
                    response = response(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"⚠️ Error: {e}")
            else:
                st.warning("I couldn't find relevant information in the document.")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "❌ I couldn't find relevant information in the document."
                })



