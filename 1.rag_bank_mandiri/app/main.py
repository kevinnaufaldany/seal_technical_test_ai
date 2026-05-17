from fastapi import FastAPI, UploadFile, File, HTTPException

from app.config import settings
from app.schemas import QueryRequest, QueryResponse, IngestResponse
from app.ingest import ingest_pdf
from app.query import answer_question


app = FastAPI(
    title="Bank Mandiri Multimodal RAG API",
    version="1.0.0",
    description="""
API untuk technical test AI Engineer Intern.

Fitur utama:
- Upload dan proses PDF Laporan Bank Mandiri 2025.
- Ekstraksi teks, tabel, dan visual knowledge.
- Penyimpanan ke ChromaDB.
- Tanya jawab berbasis RAG dengan sumber halaman.

Gunakan endpoint:
1. `/ingest` untuk upload PDF.
2. `/query` untuk bertanya ke dokumen.
""",
    docs_url="/docs",
    redoc_url=None,
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,
        "defaultModelExpandDepth": 1,
        "docExpansion": "none",
        "displayRequestDuration": True,
        "filter": False,
        "tryItOutEnabled": True,
    },
)


@app.get("/", tags=["System"], summary="API Status")
def root():
    return {
        "message": "Bank Mandiri Multimodal RAG API is running.",
        "docs": "/docs",
    }


@app.get(
    "/health",
    tags=["System"],
    summary="Health Check",
    description="Cek apakah API berjalan normal.",
)
def health_check():
    return {
        "status": "ok",
        "app_name": settings.app_name,
    }

@app.post(
    "/ingest",
    response_model=IngestResponse,
    tags=["1. Ingestion"],
    summary="Upload & Process PDF",
    description="""
Upload PDF Laporan Bank Mandiri 2025.

Pipeline:
1. Simpan file PDF.
2. Extract teks per halaman.
3. Extract tabel.
4. Tambahkan visual knowledge untuk chart/infografis.
5. Chunking.
6. Embedding.
7. Simpan ke ChromaDB.
""",
)
async def ingest_endpoint(file: UploadFile = File(...)):
    try:
        result = await ingest_pdf(file)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post(
    "/query",
    response_model=QueryResponse,
        tags=["2. Question Answering"],
    summary="Ask Question to Document",
    description="""
Ajukan pertanyaan berdasarkan dokumen yang sudah di-ingest.
""",
)
def query_endpoint(payload: QueryRequest):
    try:
        result = answer_question(
            question=payload.question,
            top_k=payload.top_k,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))