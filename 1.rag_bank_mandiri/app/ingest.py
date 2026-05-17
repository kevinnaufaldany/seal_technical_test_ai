from pathlib import Path
from shutil import copyfileobj

from fastapi import UploadFile

from app.config import settings
from app.parser import parse_pdf
from app.chunker import create_chunks
from app.vectorstore import add_documents_to_vectorstore
from app.visual_knowledge import get_visual_knowledge


async def ingest_pdf(file: UploadFile) -> dict:
    if not file.filename:
        raise ValueError("File tidak memiliki nama.")

    if not file.filename.lower().endswith(".pdf"):
        raise ValueError("File harus berupa PDF.")

    upload_path = Path(settings.upload_dir) / file.filename

    with upload_path.open("wb") as buffer:
        copyfileobj(file.file, buffer)

    parsed_docs = parse_pdf(
        pdf_path=str(upload_path),
        image_output_dir=settings.extracted_image_dir,
    )

    visual_docs = get_visual_knowledge(source_file=file.filename)

    all_docs = parsed_docs + visual_docs

    chunks = create_chunks(all_docs)
    add_documents_to_vectorstore(chunks)

    return {
        "filename": file.filename,
        "saved_path": str(upload_path),
        "total_documents": len(all_docs),
        "total_chunks": len(chunks),
        "message": "PDF berhasil diproses, visual knowledge ditambahkan, dan disimpan ke vector database.",
    }