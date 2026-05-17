# RAG Bank Mandiri - Multimodal Retrieval-Augmented Generation System

A production-ready Retrieval-Augmented Generation (RAG) system built with **FastAPI**, **LangChain**, **ChromaDB**, and **Ollama** for intelligent document retrieval and question answering over Bank Mandiri financial reports.

## 📋 Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [System Flows](#system-flows)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

RAG Bank Mandiri is a multimodal RAG system designed to process Bank Mandiri financial reports and answer user questions with precise source citations. The system extracts text, tables, and visual information from PDF documents, stores them in a vector database, and retrieves relevant context to generate accurate answers using a local LLM.

### Key Features

- ✅ **PDF Document Processing** - Extract text, tables, and visual elements from PDF files
- ✅ **Multimodal Support** - Handle text, charts, tables, and infographics with visual knowledge captions
- ✅ **Vector Retrieval** - Semantic search using embeddings stored in ChromaDB
- ✅ **Page-Aware Routing** - Intelligent detection of relevant document pages
- ✅ **Source Attribution** - Every answer includes the source page for transparency
- ✅ **Local LLM Processing** - Use Ollama models without requiring API keys
- ✅ **Interactive Swagger UI** - Test endpoints directly via `http://127.0.0.1:8000/docs`
- ✅ **Debug Mode** - Retrieve intermediate context for system transparency

---

## 🏗️ System Architecture

### High-Level Architecture Diagram

```
┌──────────────┐
│ Swagger UI   │
│ /docs        │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────┐
│ FastAPI Backend              │
│ app/main.py                  │
└──────┬───────────────────────┘
       │
       ├─────────────────────────────┐
       │                             │
       ▼                             ▼
┌──────────────────┐        ┌──────────────────┐
│ Ingestion Module │        │ Query Module     │
│ app/ingest.py    │        │ app/query.py     │
└──────┬───────────┘        └──────┬───────────┘
       │                           │
       ▼                           ▼
┌──────────────────┐        ┌──────────────────┐
│ PDF Parser       │        │ Retriever        │
│ app/parser.py    │        │ ChromaDB Search  │
└──────┬───────────┘        └──────┬───────────┘
       │                           │
       ▼                           ▼
┌──────────────────┐        ┌──────────────────┐
│ Chunker          │        │ LLM Generator    │
│ app/chunker.py   │        │ Ollama llama3.2  │
└──────┬───────────┘        └──────┬───────────┘
       │                           │
       ▼                           ▼
┌──────────────────────────────────────────────┐
│ Vector Store                                 │
│ ChromaDB + Ollama nomic-embed-text           │
└──────────────────────────────────────────────┘
```

### Main Data Flow

```
PDF Upload
   ↓
Text, Table & Visual Extraction
   ↓
Visual Knowledge Captioning
   ↓
Chunking + Metadata
   ↓
Embedding with Ollama
   ↓
Store in ChromaDB
   ↓
User Question
   ↓
Page-aware Retrieval
   ↓
LLM Answer Generation
   ↓
Answer + Source Page
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Ollama installed and running
  - Download from [ollama.ai](https://ollama.ai)
  - Pull required models: `ollama pull llama3.2` and `ollama pull nomic-embed-text`

### Installation

```bash
# Clone or navigate to the project
cd rag_bank_mandiri

# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # On Windows
# or
source venv/bin/activate      # On Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### Start the Application

```bash
# Make sure Ollama is running first
# Then start FastAPI server
uvicorn app.main:app --reload

# Server will start at http://127.0.0.1:8000
# Swagger UI available at http://127.0.0.1:8000/docs
```

### Upload Your First Document

1. Open `http://127.0.0.1:8000/docs`
2. Click on `/ingest` endpoint
3. Upload a PDF file (e.g., Bank Mandiri financial report)
4. Check the response with document statistics

### Ask Your First Question

1. In Swagger UI, go to `/query` endpoint
2. Enter your question: `"What is the DPK composition?"`
3. Check the response with answer and source page

---

## 📦 Installation

### Step-by-Step Setup

#### 1. Prerequisites Installation

```bash
# Install Python dependencies
pip install -r requirements.txt

# Verify Ollama models are available
ollama pull llama3.2
ollama pull nomic-embed-text
```

#### 2. Environment Setup

Create `.env` file (optional, for configuration):

```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL=llama3.2
EMBEDDING_MODEL=nomic-embed-text

# ChromaDB Configuration
CHROMA_PERSIST_DIR=./data/chroma
```

#### 3. Verify Installation

```bash
# Check FastAPI installation
python -c "import fastapi; print(fastapi.__version__)"

# Check LangChain installation
python -c "import langchain; print(langchain.__version__)"

# Check Ollama is running
curl http://localhost:11434/api/tags
```

---

## 💻 Usage

### General Workflow

#### 1. Ingest PDF Documents

```python
# Via Swagger UI or curl
curl -X POST "http://127.0.0.1:8000/ingest" \
  -H "accept: application/json" \
  -F "file=@path/to/document.pdf"
```

**Response:**
```json
{
  "filename": "document.pdf",
  "message": "Document ingested successfully",
  "total_documents": 12,
  "total_chunks": 156
}
```

#### 2. Query the System

```python
# Via Swagger UI or curl
curl -X POST "http://127.0.0.1:8000/query" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the DPK composition in 2024?",
    "top_k": 5,
    "answer_style": "detailed"
  }'
```

**Response:**
```json
{
  "question": "What is the DPK composition in 2024?",
  "answer": "Based on Bank Mandiri's financial report, the DPK composition in 2024 is: Giro and Giro Wadiah 39.31%, Tabungan and Tabungan Wadiah 40.12%, Deposito Berjangka 20.57%",
  "sources": [
    {
      "page": 6,
      "filename": "Laporan Keuangan Bank Mandiri 2025.pdf",
      "content_type": "text"
    }
  ]
}
```

#### 3. Debug Mode

For transparency and debugging, use `answer_style: "debug"`:

```json
{
  "question": "What is the DPK composition?",
  "top_k": 5,
  "answer_style": "debug"
}
```

This will include `retrieved_contexts` showing exactly which document chunks were used.

---

## 🔌 API Endpoints

### 1. Health Check

**Endpoint:** `GET /health`

**Description:** Check if the API is running and vector database is accessible

**Response:**
```json
{
  "status": "healthy",
  "message": "API is running and ChromaDB is accessible"
}
```

---

### 2. Ingest PDF

**Endpoint:** `POST /ingest`

**Description:** Upload and process a PDF document

**Request:**
- `file` (required): PDF file to upload

**Response:**
```json
{
  "filename": "string",
  "message": "string",
  "total_documents": "integer",
  "total_chunks": "integer"
}
```

**Example:**
```bash
curl -X POST "http://127.0.0.1:8000/ingest" \
  -F "file=@financial_report.pdf"
```

**Process Flow:**
1. Validate file type (must be PDF)
2. Save to `data/uploads/`
3. Extract text, tables, and render page images
4. Generate visual knowledge captions
5. Chunk document with metadata
6. Create embeddings with Ollama
7. Store in ChromaDB

---

### 3. Query/RAG

**Endpoint:** `POST /query`

**Description:** Ask questions about ingested documents

**Request:**
```json
{
  "question": "string (required)",
  "top_k": "integer (default: 5)",
  "answer_style": "concise | detailed | debug (default: detailed)"
}
```

**Response:**
```json
{
  "question": "string",
  "answer": "string",
  "sources": [
    {
      "page": "integer",
      "filename": "string",
      "content_type": "string"
    }
  ],
  "retrieved_contexts": "optional array (only if answer_style=debug)"
}
```

**Example:**
```bash
curl -X POST "http://127.0.0.1:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Bagaimana alur pengaduan nasabah?",
    "top_k": 5,
    "answer_style": "detailed"
  }'
```

**Answer Styles:**
- `concise`: Ringkas, hanya informasi pokok
- `detailed`: Lengkap dengan konteks tambahan
- `debug`: Tampilkan retrieved_contexts untuk debugging

---

## 📊 System Flows

### Flow 1: Document Ingestion Pipeline

```
START
  │
  ▼
User upload PDF ke endpoint /ingest
  │
  ▼
Validasi file (must be PDF)
  │
  ├── Bukan PDF? ──► Return error 400
  │
  ▼
Simpan PDF ke folder data/uploads
  │
  ▼
Parse PDF dengan pdfplumber dan PyMuPDF
  │
  ├── Extract teks per halaman
  │
  ├── Extract tabel
  │
  └── Render halaman PDF menjadi image PNG
  │
  ▼
Tambahkan visual_knowledge.py
  │
  ├── Caption tabel sektor ekonomi halaman 4
  │
  ├── Caption chart DPK halaman 6
  │
  ├── Caption infografis pengaduan halaman 8
  │
  └── Caption saluran pengaduan halaman 9
  │
  ▼
Gabungkan parsed_docs + visual_docs
  │
  ▼
Chunking dengan RecursiveCharacterTextSplitter
  │
  ├── chunk_size: 1024
  │
  └── chunk_overlap: 256
  │
  ▼
Buat embedding dengan OllamaEmbeddings
  │
  ├── Model: nomic-embed-text
  │
  └── Batch processing untuk efisiensi
  │
  ▼
Simpan chunk + metadata ke ChromaDB
  │
  ├── Metadata: source_file, page, content_type
  │
  └── Persist ke disk di data/chroma/
  │
  ▼
Return response:
- filename
- total_documents
- total_chunks
- message
  │
  ▼
END
```

### Flow 2: Query/RAG Pipeline

```
START
  │
  ▼
User kirim pertanyaan ke endpoint /query
  │
  ▼
Terima input:
- question
- top_k
- answer_style
  │
  ▼
Query Expansion (jika diperlukan)
Tambahkan keyword tambahan untuk coverage lebih luas
  │
  ▼
Detect target page
  │
  ├── Pertanyaan tentang Tambang/Konstruksi → page 4
  │
  ├── Pertanyaan tentang DPK → page 6
  │
  ├── Pertanyaan tentang Pelindungan Nasabah → page 7
  │
  ├── Pertanyaan tentang Penagihan → page 7
  │
  ├── Pertanyaan tentang Alur pengaduan → page 8
  │
  └── Pertanyaan tentang Saluran pengaduan → page 9
  │
  ▼
Retrieve documents dari ChromaDB
  │
  ├── Prioritize visual captions terlebih dahulu
  │
  ├── Lakukan similarity search dengan embedding pertanyaan
  │
  ├── Ambil top_k dokumen paling relevan
  │
  └── Deduplicate hasil retrieval
  │
  ▼
Format context untuk LLM
  │
  ├── Urutkan chunk berdasarkan relevansi
  │
  └── Siapkan prompt template
  │
  ▼
Pilih gaya jawaban
  │
  ├── concise → instruksi untuk jawaban singkat
  │
  ├── detailed → instruksi untuk jawaban lengkap
  │
  └── debug → include retrieved_contexts dalam response
  │
  ▼
Kirim prompt + context ke LLM Ollama
  │
  ├── Model: llama3.2
  │
  └── Temperature: 0.7
  │
  ▼
LLM menghasilkan jawaban
  │
  ▼
Build sources dari metadata
  │
  ├── Ambil unique pages dari retrieved chunks
  │
  ├── Ambil filename dan content_type
  │
  └── Format untuk response
  │
  ▼
Return response:
{
  "question": ...,
  "answer": ...,
  "sources": [...],
  "retrieved_contexts": ... (jika debug mode)
}
  │
  ▼
END
```

### Flow 3: Swagger UI Usage Flow

```
┌─────────────────────────────┐
│ User membuka browser        │
│ http://127.0.0.1:8000/docs  │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Tampil Swagger UI           │
│ Dokumentasi endpoint        │
└──────────────┬──────────────┘
               │
               ├─────────────────────────┐
               │                         │
               ▼                         ▼
    ┌──────────────────┐      ┌──────────────────┐
    │ Cek /health      │      │ Upload /ingest   │
    └──────────────────┘      └────────┬─────────┘
                                       │
                                       ▼
                              ┌──────────────────┐
                              │ Pilih file PDF   │
                              └────────┬─────────┘
                                       │
                                       ▼
                              ┌──────────────────┐
                              │ Click "Execute"  │
                              └────────┬─────────┘
                                       │
                                       ▼
                              ┌──────────────────┐
                              │ Lihat response   │
                              │ status, chunks   │
                              └────────┬─────────┘
                                       │
                                       ▼
                              ┌──────────────────┐
                              │ Test /query      │
                              └────────┬─────────┘
                                       │
                                       ▼
                              ┌──────────────────┐
                              │ Input question   │
                              │ Pilih top_k & style
                              └────────┬─────────┘
                                       │
                                       ▼
                              ┌──────────────────┐
                              │ Click "Execute"  │
                              └────────┬─────────┘
                                       │
                                       ▼
                              ┌──────────────────┐
                              │ Lihat jawaban    │
                              │ sumber halaman   │
                              │ (debug: context) │
                              └──────────────────┘
```

---

## 📁 Project Structure

```
rag_bank_mandiri/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── app/
│   ├── __init__.py
│   ├── main.py                       # FastAPI entry point, endpoint definitions
│   ├── config.py                     # Configuration, model paths, hyperparameters
│   ├── schemas.py                    # Pydantic models for request/response
│   ├── parser.py                     # PDF parsing, text/table extraction
│   ├── chunker.py                    # Document chunking with LangChain
│   ├── vectorstore.py                # ChromaDB initialization and management
│   ├── ingest.py                     # Ingestion pipeline orchestration
│   ├── query.py                      # Query/RAG pipeline orchestration
│   └── visual_knowledge.py           # Visual caption generation for charts/tables
├── data/
│   ├── uploads/                      # User uploaded PDF files
│   ├── extracted_images/             # Rendered PDF page images
│   └── chroma/                       # ChromaDB persistent storage
│       ├── chroma.sqlite3            # Vector database file
│       └── [collection_uuid]/        # Collection data
└── .env                              # Environment variables (optional)
```

### File Descriptions

| File | Purpose |
|------|---------|
| `app/main.py` | FastAPI app initialization, endpoints `/health`, `/ingest`, `/query` |
| `app/config.py` | Configuration constants (model names, paths, chunk sizes) |
| `app/schemas.py` | Pydantic models: `IngestResponse`, `QueryRequest`, `QueryResponse` |
| `app/parser.py` | PDF text/table extraction using pdfplumber and PyMuPDF |
| `app/chunker.py` | `RecursiveCharacterTextSplitter` for document splitting |
| `app/vectorstore.py` | ChromaDB client setup and collection management |
| `app/ingest.py` | Complete ingestion workflow (parse → chunk → embed → store) |
| `app/query.py` | Complete query workflow (retrieve → generate → format response) |
| `app/visual_knowledge.py` | Generate structured captions for charts/infographics |

---

## 🔧 Technology Stack

### 1. **FastAPI**
- **Role:** Backend API framework
- **Why:** Fast, automatic Swagger UI, perfect for demo
- **Used in:** `app/main.py`

### 2. **LangChain**
- **Role:** Orchestration layer for LLM and embeddings
- **Components:**
  - `RecursiveCharacterTextSplitter` for chunking
  - `Document` objects for metadata
  - LLM/Embedding integration
- **Used in:** `app/chunker.py`, `app/vectorstore.py`, `app/query.py`

### 3. **pdfplumber**
- **Role:** PDF text and table extraction
- **Why:** Reliable for financial documents with tables
- **Used in:** `app/parser.py`

### 4. **PyMuPDF (fitz)**
- **Role:** PDF rendering to PNG images
- **Why:** Multimodal support, visual debugging
- **Used in:** `app/parser.py`

### 5. **Ollama**
- **Role:** Local LLM and embedding models
- **Models Used:**
  - `llama3.2` - Answer generation
  - `nomic-embed-text` - Embedding creation
- **Why:** No API keys needed, offline capable

### 6. **ChromaDB**
- **Role:** Vector database
- **Why:** Simple to use, persistent storage, similarity search
- **Storage:** `data/chroma/`

### 7. **Pydantic**
- **Role:** Request/response validation
- **Used in:** `app/schemas.py`

---

## ⚙️ Configuration

### Default Configuration (`app/config.py`)

```python
# Ollama Models
LLM_MODEL = "llama3.2"
EMBEDDING_MODEL = "nomic-embed-text"
OLLAMA_BASE_URL = "http://localhost:11434"

# Chunking Parameters
CHUNK_SIZE = 1024
CHUNK_OVERLAP = 256

# ChromaDB
CHROMA_PERSIST_DIR = "./data/chroma"
COLLECTION_NAME = "bank_mandiri"

# Query Parameters
DEFAULT_TOP_K = 5
LLM_TEMPERATURE = 0.7
```

### Environment Variables (.env)

```env
# Ollama
OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL=llama3.2
EMBEDDING_MODEL=nomic-embed-text

# ChromaDB
CHROMA_PERSIST_DIR=./data/chroma

# Application
APP_DEBUG=False
APP_PORT=8000
```

### Customization Examples

#### Increase Chunk Size for Longer Context

```python
# In app/config.py
CHUNK_SIZE = 2048
CHUNK_OVERLAP = 512
```

#### Change Top-K Results

```python
# In Query Request (Swagger UI)
{
  "question": "What is DPK?",
  "top_k": 10  # Retrieve 10 instead of 5
}
```

#### Adjust LLM Temperature

```python
# In app/query.py (modify before deploy)
llm = Ollama(
    model=LLM_MODEL,
    temperature=0.3  # Lower = more focused, Higher = more creative
)
```

---

## 🐛 Troubleshooting

### Issue: Connection refused to localhost:11434

**Cause:** Ollama is not running

**Solution:**
```bash
# Start Ollama
ollama serve

# Or on macOS/Windows, check if Ollama is running in system tray
# Then verify connection
curl http://localhost:11434/api/tags
```

---

### Issue: Model not found error

**Cause:** Required Ollama models not pulled

**Solution:**
```bash
# Pull required models
ollama pull llama3.2
ollama pull nomic-embed-text

# Verify models are available
ollama list
```

---

### Issue: ChromaDB connection error

**Cause:** Corrupted database or missing directory

**Solution:**
```bash
# Reset ChromaDB (WARNING: This deletes all stored documents)
Remove-Item -Recurse -Force data\chroma
mkdir data\chroma       
# The system will recreate it on next ingest
```


---

### Issue: Out of memory during embedding

**Cause:** Batch size too large

**Solution:**
```python
# In app/config.py, reduce batch size
EMBEDDING_BATCH_SIZE = 10  # Default might be 100
```

---

### Issue: Slow retrieval

**Cause:** Large number of documents or unoptimized queries

**Solution:**
1. Filter by page before retrieval
2. Reduce `top_k` in query
3. Optimize chunk size for your use case

---

### Issue: Inaccurate answers

**Cause:** Poor retrieval or insufficient context

**Solution:**
1. Use `answer_style: "debug"` to inspect retrieved context
2. Increase `top_k` to get more context
3. Verify visual knowledge captions are being added
4. Check if important pages are being skipped

---

## 📝 Demo Narration

### Complete System Explanation

> Sistem ini memiliki dua alur utama: ingestion dan query.
>
> **Pada alur ingestion**, user mengupload PDF Laporan Bank Mandiri 2025 melalui endpoint `/ingest`. Sistem kemudian mengekstrak teks, tabel, dan menyimpan representasi visual halaman PDF. Untuk informasi berbentuk chart dan infografis, sistem menambahkan visual knowledge berupa caption terstruktur agar informasi visual dapat dicari oleh vector retrieval. Setelah itu dokumen dipotong menjadi chunk, dibuat embedding menggunakan Ollama `nomic-embed-text`, lalu disimpan ke ChromaDB bersama metadata halaman.
>
> **Pada alur query**, user mengirim pertanyaan melalui endpoint `/query`. Sistem melakukan query expansion dan page-aware routing untuk mendeteksi halaman yang kemungkinan relevan, lalu mengambil context dari ChromaDB. Context tersebut dikirim ke LLM lokal Ollama `llama3.2` untuk disintesis menjadi jawaban. Response akhir berisi jawaban, sumber halaman, dan optional `retrieved_contexts` untuk mode debug.

---

## 🎓 Key Technical Concepts

### Multimodal RAG

This system supports multiple data modalities:
- **Text:** Extracted paragraphs and sentences
- **Tables:** Structured data from financial reports
- **Visual:** Charts, infographics converted to structured captions
- **Metadata:** Page numbers, file names for source attribution

### Vector Embeddings

- Each chunk is converted to a numerical vector using `nomic-embed-text`
- Similar chunks have similar vectors
- ChromaDB performs similarity search in vector space
- User queries are embedded and compared against document vectors

### Chunking Strategy

- **Size:** 1024 tokens (default)
- **Overlap:** 256 tokens (prevents losing context at chunk boundaries)
- **Recursive:** Splits on natural boundaries (sentences, paragraphs)
- **Metadata:** Preserves page numbers for source citation

### Local LLM Pipeline

1. Retrieve relevant context from ChromaDB
2. Format context into system prompt
3. Send to local Ollama instance
4. Generate answer without external API calls
5. Extract and format response

---

## 📚 References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Ollama Documentation](https://github.com/ollama/ollama)
- [pdfplumber Documentation](https://github.com/jsvine/pdfplumber)

---

## 📄 License

This project is part of a technical test for candidate as AI Engineer Intern in SEAL.

---

## 👤 Author

Created as a complete multimodal RAG system for technical assessment.

---

## 🤝 Contributing

For improvements or bug fixes, please document:
1. What was changed
2. Why it was changed
3. How to test the change
4. Any new dependencies added

---

## ✅ Checklist for First-Time Setup

- [ ] Python 3.9+ installed
- [ ] Virtual environment created and activated
- [ ] `pip install -r requirements.txt` completed
- [ ] Ollama installed and running (`ollama serve`)
- [ ] Required models pulled (`ollama pull llama3.2`, `ollama pull nomic-embed-text`)
- [ ] FastAPI server starts without errors (`uvicorn app.main:app --reload`)
- [ ] Swagger UI accessible at `http://127.0.0.1:8000/docs`
- [ ] Test `/health` endpoint returns successful response
- [ ] Upload test PDF via `/ingest` endpoint
- [ ] Query system via `/query` endpoint with test question

---

**Last Updated:** May 2025  
**System Version:** 1.0  
**Status:** Production Ready
