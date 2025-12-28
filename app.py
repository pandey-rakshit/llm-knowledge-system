import streamlit as st

from ui.chat_interface import ChatInterface
from ui.components import (
    add_message,
    display_chat_history,
    display_sidebar,
    init_session_state,
)

st.set_page_config(
    page_title="Hybrid RAG Search Engine",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main():
    init_session_state()

    if "chat_interface" not in st.session_state:
        st.session_state.chat_interface = ChatInterface()

    if "web_enabled" not in st.session_state:
        st.session_state.web_enabled = False

    if "include_wikipedia" not in st.session_state:
        st.session_state.include_wikipedia = False

    chat = st.session_state.chat_interface

    display_sidebar()

    st.title("🤖 Hybrid RAG Search Engine")
    st.markdown("📄 Documents • 🌐 Web • 🔀 Hybrid")

    st.divider()

    display_chat_history()

    if prompt := st.chat_input("Ask a question..."):
        add_message("user", prompt)

        with st.chat_message("user"):
            st.markdown(prompt)

        answer, sources = chat.answer(
            prompt, st.session_state.web_enabled, st.session_state.include_wikipedia
        )

        add_message("assistant", answer, sources)

        with st.chat_message("assistant"):
            st.markdown(answer)
            if sources:
                with st.expander("📚 Sources"):
                    for src in sources:
                        st.markdown(f"- {src}")

    st.divider()
    with st.container():
        st.session_state.web_enabled = st.toggle(
            "🌐 Enable Web Search",
            value=False,
            help="Use Tavily for real-time information",
        )

        if st.session_state.web_enabled:
            st.session_state.include_wikipedia = st.toggle(
                "Enable Wikipedia", value=False, help="Use Wikipedia for source"
            )

    with st.expander(
        "📤 Upload Documents", expanded=not st.session_state.vector_store_initialized
    ):
        uploaded_files = st.file_uploader(
            "Upload PDF / TXT / MD files",
            type=["pdf", "txt", "md"],
            accept_multiple_files=True,
        )

        if uploaded_files and st.button("Process Documents", type="primary"):
            with st.spinner("Indexing documents..."):
                count = chat.process_documents(uploaded_files)
                st.success(f"Indexed {count} chunks")
                st.rerun()


if __name__ == "__main__":
    main()
