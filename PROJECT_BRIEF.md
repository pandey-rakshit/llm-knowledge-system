# **GA02: Multi-Document RAG Search Engine (with Real-Time Web Search)**

## **Background**

You are working as an AI Engineer at a Knowledge Intelligence startup that builds internal search and question-answering tools for enterprises, research teams, and educational institutions.

Organizations store knowledge across **multiple unstructured documents** such as PDFs, reports, notes, and reference materials. However, **static document knowledge alone is often insufficient**—users also need **up-to-date, real-world information**.

Common challenges include:

- Searching across multiple documents and sources
- Answering questions that combine **internal documents + live web data**
- Distinguishing between **document-grounded answers** and **real-time facts**
- Trusting answers through transparent citations

Your task is to build a **Hybrid RAG Search Engine** that combines:

- **Multi-document semantic search**
- **Retrieval-Augmented Generation (RAG)**
- **Real-time web search using Tavily**

This project mirrors real-world enterprise copilots and research assistants that blend **private knowledge bases with live internet search**.

---

## **Objective**

Your objective is to design and implement a **medium-complexity hybrid RAG system** that:

- Builds a searchable knowledge base from multiple documents
- Uses FAISS for semantic vector search
- Integrates **Tavily Search** for real-time queries
- Dynamically decides between **document search vs web search**
- Returns grounded answers with **clear source attribution**
- Provides a clean **Streamlit-based chatbot UI**

By the end of this project, you should demonstrate:

- Multi-source retrieval design
- Hybrid RAG architectures
- Citation-aware answer generation
- Practical LangChain tool integration
- End-user AI application design

---

## **Tech Stack (Strictly Enforced)**

- **Programming Language:** Python
- **LLM Orchestration:** LangChain
- **Vector Database:** FAISS
- **Web Search Tool:** Tavily Search (via LangChain)
- **Frontend / UI:** Streamlit

---

## **Data Sources**

### **Local Knowledge Base**

- PDF documents
- Text / Markdown files
- Wikipedia pages (LangChain loaders)

### **Real-Time Knowledge**

- Tavily web search results:
    - Current events
    - Recent research
    - Live statistics
    - News or factual updates

---

## **Part I: Document Ingestion & Representation**

### **1. Unified Document Schema**

Design a unified schema that supports both **local documents** and **web results**.

Each document or chunk should include:

- `source_id`
- `source_type` (pdf / wikipedia / web)
- `title`
- `content`
- `metadata`

Task:

Define Python data models for:

- Document
- DocumentChunk
- WebSearchResult
- AnswerSource

---

### **2. Multi-Source Document Loading**

Using LangChain loaders:

- Load multiple PDFs
- Load Wikipedia pages
- Load text files

Ensure:

- Metadata consistency
- Source traceability

Deliverable:

A document ingestion pipeline producing normalized documents.

---

### **3. Text Cleaning & Normalization**

Perform:

- Noise removal
- Whitespace normalization
- Artifact filtering

Reflection Question:

Why does noisy text reduce embedding quality and retrieval accuracy?

---

## **Part II: Chunking & Vector Indexing**

### **4. Chunking Strategy**

Split documents using:

- Recursive character chunking
- Overlapping windows

Metadata per chunk:

- Document title
- Chunk index
- Source type

---

### **5. FAISS Vector Store Construction**

Using LangChain + FAISS:

- Generate embeddings
- Store vectors with metadata
- Persist index locally

Functions to implement:

- `index_documents()`
- `load_faiss_index()`

---

### **6. Semantic Search Across Documents**

Implement semantic search that:

- Accepts natural language queries
- Searches across all indexed documents
- Returns top-K chunks

---

## **Part III: Hybrid RAG Pipeline (Documents + Web)**

### **7. Query Classification Logic**

Before retrieval, classify queries into:

- **Document-based queries**
- **Real-time web queries**
- **Hybrid queries**

Example:

- “Explain attention mechanism” → Document search
- “Latest developments in GPT models” → Tavily search
- “How does RAG compare with current LLM tools?” → Hybrid

Deliverable:

A lightweight query routing function.

---

### **8. Tavily Web Search Integration**

Using Tavily via LangChain:

- Execute real-time web searches
- Retrieve:
    - Page titles
    - Snippets
    - URLs

Ensure:

- Results are treated as **temporary documents**
- Stored separately from FAISS index

---

### **9. Context Assembly for RAG**

Construct context by combining:

- FAISS-retrieved document chunks
- Tavily search snippets (if applicable)

Apply:

- Context size limits
- Source tagging

---

### **10. Question Answering with Citations**

Generate answers that:

- Are grounded in retrieved content
- Clearly distinguish:
    - **Document sources**
    - **Web sources**

Citation format example:

```
[Doc] Transformer Notes.pdf – Chunk3
[Web] Tavily: “Recent Advancesin RAG Systems”

```

---

### **11. Top-N Document Summaries**

For each query:

- Identify top-N documents
- Generate concise summaries
- Display summaries with citations

---

## **Part IV: Streamlit UI Development**

### **12. Document Management Sidebar**

Features:

- Upload documents
- View indexed files
- Toggle Tavily search ON/OFF

---

### **13. Hybrid Chat Interface**

Main panel:

- Chat input
- Real-time responses
- Source-aware answers

Visual indicators:

- 📄 Document-based answer
- 🌐 Web-based answer
- 🔀 Hybrid answer

---

### **14. Evidence & Source Tabs**

Streamlit tabs for:

- Answer
- Document evidence
- Web evidence

This ensures transparency and explainability.

---

## **Part V: Evaluation & Reporting**

### **15. Scenario-Based Evaluation**

Test scenarios:

- Static knowledge queries
- Real-time factual queries
- Hybrid reasoning queries

---

### **16. Quality Assessment**

Evaluate:

- Retrieval relevance
- Answer grounding
- Web vs document separation
- Citation clarity

Document:

- Strengths
- Limitations
- Future enhancements

---

## **Final Deliverables**

### **Backend**

- Document ingestion pipeline
- FAISS vector index
- Tavily web search integration
- Hybrid RAG logic

### **Frontend**

- Streamlit document manager
- Hybrid chatbot UI
- Evidence and citation display

### **Documentation**

- Architecture diagram
- Design rationale
- Example queries
- Evaluation report

---

## **Key Learning Outcomes**

By completing this project, students will demonstrate:

✅ Multi-document RAG system design

✅ Hybrid retrieval (vector + web)

✅ Tavily real-time search integration

✅ Citation-aware answer generation

✅ Practical LangChain + Streamlit skills