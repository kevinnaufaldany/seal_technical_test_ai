from typing import Any

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def create_chunks(parsed_docs: list[dict[str, Any]]) -> list[Document]:
    """
    Convert parsed document dictionaries into LangChain Documents and chunk them.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=180,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )

    all_chunks: list[Document] = []

    for doc_idx, item in enumerate(parsed_docs):
        content = item["content"]
        metadata = item["metadata"]

        base_doc = Document(
            page_content=content,
            metadata={
                **metadata,
                "doc_id": doc_idx,
            },
        )

        chunks = splitter.split_documents([base_doc])

        for chunk_idx, chunk in enumerate(chunks):
            chunk.metadata["chunk_id"] = f"{doc_idx}-{chunk_idx}"
            all_chunks.append(chunk)

    return all_chunks