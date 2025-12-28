import os
from typing import Optional

import streamlit as st

from config import settings

UPLOAD_DIR = settings.UPLOAD_DIR
os.makedirs(UPLOAD_DIR, exist_ok=True)


def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = []

    if "vector_store_initialized" not in st.session_state:
        st.session_state.vector_store_initialized = False


def add_message(role: str, content: str, sources: Optional[str] = None):
    st.session_state.messages.append(
        {"role": role, "content": content, "sources": sources}
    )


def display_chat_history():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("sources"):
                with st.expander("📚 sources"):
                    for src in message["sources"]:
                        st.markdown(f"- {src}")


def clear_chat():
    st.session_state.messages = []


def save_uploaded_file(uploaded_file) -> str:
    print(f"uploaded file:", uploaded_file)
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path


def delete_uploaded_file(filename: str):
    path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(path):
        os.remove(path)


def display_sidebar():
    with st.sidebar:
        st.header("📄 Document RAG Chatbot")

        st.markdown(
            """
        **How it works**
        1. Upload documents
        2. Ask questions
        3. Answers are grounded in your files
        """
        )

        st.divider()

        st.subheader("Uploaded Files")
        if st.session_state.uploaded_files:
            for f in st.session_state.uploaded_files:
                col1, col2 = st.columns([7, 2])
                col1.write(f)
                if col2.button("", key=f"del_{f}", icon="🗑️"):
                    st.session_state.chat_interface.delete_document(f)
                    st.rerun()
        else:
            st.write("No files uploaded")

        st.divider()

        if st.button("🗑️ Clear Chat"):
            clear_chat()
            st.rerun()
