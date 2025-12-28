import streamlit as st

from core.chain import RAGChain
from core.document import DocumentProcessor, WikipediaDocumentLoader
from core.retriever import RetrieverService
from core.vectorstore import VectorStoreService
from ui.components import delete_uploaded_file, save_uploaded_file


class ChatInterface:
    def __init__(self):
        self.doc_processor = DocumentProcessor()
        self.vector_store = VectorStoreService()
        self.retriever_service = RetrieverService(self.vector_store)
        self.rag_chain = RAGChain(self.retriever_service)
        self.wiki_loader = WikipediaDocumentLoader()

    def process_documents(self, uploaded_files) -> int:
        all_chunks = []

        for uploaded_file in uploaded_files:
            print(uploaded_file)
            path = save_uploaded_file(uploaded_file)
            chunks = self.doc_processor.process(path)

            for chunk in chunks:
                chunk["metadata"]["title"] = uploaded_file.name

            all_chunks.extend(chunks)

            if uploaded_file.name not in st.session_state.uploaded_files:
                st.session_state.uploaded_files.append(uploaded_file.name)

        if all_chunks:
            self.vector_store.add_documents(all_chunks)
            st.session_state.vector_store_initialized = True

        return len(all_chunks)

    def answer(self, query: str, web_enabled: bool, include_wikipedia: bool = False):
        wiki_docs = []
        if include_wikipedia:
            wiki_docs = self.wiki_loader.load(query)

        result = self.rag_chain.run(query, web_enabled, wiki_docs)
        return result["answer"], result["sources"]

    def delete_document(self, filename: str):
        self.vector_store.remove_document(filename)
        delete_uploaded_file(filename)

        if filename in st.session_state.uploaded_files:
            st.session_state.uploaded_files.remove(filename)
