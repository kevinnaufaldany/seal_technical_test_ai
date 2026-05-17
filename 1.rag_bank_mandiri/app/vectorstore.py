from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

from app.config import settings


def get_embedding_model() -> OllamaEmbeddings:
    return OllamaEmbeddings(
        model=settings.ollama_embedding_model,
    )


def get_vectorstore() -> Chroma:
    embeddings = get_embedding_model()

    return Chroma(
        collection_name=settings.collection_name,
        persist_directory=settings.chroma_dir,
        embedding_function=embeddings,
    )


def add_documents_to_vectorstore(documents):
    vectorstore = get_vectorstore()
    vectorstore.add_documents(documents)
    return vectorstore


def similarity_search(question: str, top_k: int = 5):
    vectorstore = get_vectorstore()
    return vectorstore.similarity_search(question, k=top_k)


def similarity_search_by_page(question: str, page: int, top_k: int = 5):
    vectorstore = get_vectorstore()

    return vectorstore.similarity_search(
        question,
        k=top_k,
        filter={"page": page},
    )


def get_documents_by_page(page: int) -> list[Document]:
    """
    Ambil semua chunks pada halaman tertentu.
    Ini penting untuk pertanyaan yang sudah jelas sumber halamannya.
    """
    vectorstore = get_vectorstore()

    result = vectorstore.get(
        where={"page": page},
        include=["documents", "metadatas"],
    )

    documents = result.get("documents", [])
    metadatas = result.get("metadatas", [])

    docs: list[Document] = []

    for content, metadata in zip(documents, metadatas):
        docs.append(
            Document(
                page_content=content,
                metadata=metadata,
            )
        )

    return docs


def deduplicate_documents(docs: list[Document]) -> list[Document]:
    seen = set()
    unique_docs = []

    for doc in docs:
        metadata = doc.metadata
        key = (
            metadata.get("source_file"),
            metadata.get("page"),
            metadata.get("content_type"),
            metadata.get("chunk_id"),
            doc.page_content[:80],
        )

        if key not in seen:
            seen.add(key)
            unique_docs.append(doc)

    return unique_docs