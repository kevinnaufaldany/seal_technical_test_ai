from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class QueryRequest(BaseModel):
    question: str = Field(
        ...,
        description="Pertanyaan user berdasarkan dokumen Bank Mandiri.",
        examples=[
            "Apa saja saluran pengaduan yang disediakan oleh Bank Mandiri?"
        ],
    )
    top_k: int = Field(
        default=12,
        description="Jumlah context yang diambil dari vector database.",
        ge=1,
        le=20,
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "question": "Apa saja saluran pengaduan yang disediakan oleh Bank Mandiri?",
                "top_k": 12,
            }
        }
    )


class SourceMetadata(BaseModel):
    source_file: str | None = None
    page: int | None = None
    content_type: str | None = None
    chunk_id: str | None = None


class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: list[dict[str, Any]]
    retrieved_contexts: list[str]


class IngestResponse(BaseModel):
    filename: str
    saved_path: str
    total_documents: int
    total_chunks: int
    message: str