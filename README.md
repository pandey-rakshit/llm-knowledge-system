# 🧠 LLM Knowledge System (Hybrid RAG Search Engine)

A generic LLM knowledge system that integrates documents, web search, and multiple LLM providers with grounded, source-aware answers.

**Documents • Web • Hybrid Retrieval using LLMs**

An **open-source Hybrid Retrieval-Augmented Generation (RAG) system** built with **Streamlit, LangChain, FAISS, and modern LLM providers**.
This project enables users to upload documents, index them semantically, and ask questions grounded in **their private data**, optionally enriched with **real-time web search**.

> 📜 **License:** MIT — free to use, modify, and distribute.

---

## ✨ Features

* 📄 Upload multiple document types (`PDF`, `TXT`, `MD`)
* 🔍 Semantic search using **FAISS vector store**
* 🧠 LLM-powered answers with **source attribution**
* 🌐 Optional real-time web search (Hybrid RAG)
* 💬 Chat-based interface (Streamlit)
* 🧱 Modular, extensible architecture
* 🧪 Designed for experimentation & learning

---

## 🏗️ High-Level Architecture

```
┌──────────────┐
│  Streamlit UI│
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│  Chat Interface       │
│  (Orchestrator)       │
└──────┬───────────────┘
       │
       ├──► Document Processing
       │     (Load → Chunk → Embed)
       │
       ├──► Vector Store (FAISS)
       │
       ├──► Retriever
       │     (Semantic / Hybrid)
       │
       └──► LLM
             (Answer Generation)
```

---

## 🧩 Core Components Explained

### 1️⃣ Streamlit UI (Frontend)

Responsible for:

* File upload
* Chat input/output
* Sidebar (uploaded files, controls)
* Feature toggles (web search, Wikipedia, etc.)

**Key principle:**
UI widgets are **stateless**; all persistence happens via controlled session state and backend services.

---

### 2️⃣ Document Upload & Storage

**What happens when you upload a file:**

1. User uploads documents via `st.file_uploader`
2. Files are temporarily saved to `UPLOAD_DIR`
3. Only **filenames** are stored in session state
4. Actual file contents are processed and indexed

This avoids mixing:

* UI objects (`UploadedFile`)
* Persistent application state (`str`, metadata)

---

### 3️⃣ Document Processing Pipeline

Each document goes through the following stages:

```
Raw File
  ↓
Document Loader
  ↓
Text Chunking
  ↓
Embedding Generation
  ↓
Vector Store Indexing
```

#### 🔹 Loaders

* PDF → `PyPDFLoader`
* TXT / MD → `TextLoader`

#### 🔹 Chunking

* Uses `RecursiveCharacterTextSplitter`
* Configurable `chunk_size` and `chunk_overlap`
* Preserves semantic boundaries

#### 🔹 Embeddings

* Powered by Hugging Face / Sentence Transformers
* Converts text chunks into dense vectors

---

### 4️⃣ Vector Store (FAISS)

* Stores embeddings locally
* Enables fast similarity search
* Designed for **offline, private, low-latency retrieval**

Each chunk is stored with:

* Content
* Source filename
* Metadata (chunk index, type)

---

### 5️⃣ Retriever Layer

Two modes are supported:

#### 📄 Document-Only RAG

* Searches only uploaded documents

#### 🌐 Hybrid RAG

* Combines:

  * Vector store results
  * Optional web search (Tavily / Wikipedia)

Retriever selects **most relevant context** before passing it to the LLM.

---

### 6️⃣ LLM Layer

Responsible for:

* Understanding the user query
* Consuming retrieved context
* Generating a grounded answer
* Returning cited sources

The architecture supports:

* Groq `(Implemented)`
* OpenAI
* OpenRouter
* Gemini
* Any LangChain-compatible LLM

---

### 7️⃣ Chat Memory & State

* Chat history is stored in `st.session_state`
* Each message contains:

  * Role (`user` / `assistant`)
  * Content
  * Sources (if available)

This enables:

* Conversational flow
* Context-aware follow-up questions

---

## 🔄 End-to-End Flow

```
User uploads documents
        ↓
Documents saved temporarily
        ↓
Text chunked & embedded
        ↓
Embeddings stored in FAISS
        ↓
User asks a question
        ↓
Retriever fetches relevant context
        ↓
LLM generates grounded answer
        ↓
Answer + sources shown in chat
```

---

## 🛠️ Tech Stack

| Layer         | Technology             |
| ------------- | ---------------------- |
| UI            | Streamlit              |
| LLM Framework | LangChain              |
| Vector DB     | FAISS                  |
| Embeddings    | Hugging Face           |
| LLM Providers | Groq / OpenAI / Gemini |
| Web Search    | Tavily / Wikipedia     |
| Language      | Python 3.10+           |

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/hybrid-rag-search-engine.git
cd hybrid-rag-search-engine
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
.venv\Scripts\activate     # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure Environment Variables

Create a `.env` file:

```env
LLM_PROVIDER=groq
GROQ_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
```

---

### 5️⃣ Run the App

```bash
streamlit run app.py
```

---

## ⚙️ Configuration

All tunable parameters live in `config/settings.py`:

* Chunk size & overlap
* Upload directory
* Embedding model
* Vector store settings

---

## 🧪 Use Cases

* Research paper Q&A
* Internal document search
* Knowledge base assistants
* Learning RAG systems
* Prototyping LLM applications

---

## 🔐 Privacy & Security

* All uploaded documents stay **local**
* No data is sent externally unless:

  * Web search is explicitly enabled
* Vector store is stored locally

---

## 📦 Extensibility

You can easily add:

* New document types
* New LLM providers
* Reranking models
* Persistent vector stores
* Authentication
* Multi-user support

---

## 🤝 Contributing

Contributions are welcome!

* Fork the repo
* Create a feature branch
* Submit a PR with clear description

---

## 📜 License

This project is licensed under the **MIT License**.
You are free to use, modify, and distribute it.

---

## 🧠 Final Note

This project is intentionally designed to be:

* **Readable**
* **Modular**
* **Educational**
* **Production-aligned**

If you understand this architecture, you understand **real-world RAG systems**.