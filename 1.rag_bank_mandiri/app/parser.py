from pathlib import Path
from typing import Any

import fitz
import pdfplumber


def extract_tables_from_page(page: pdfplumber.page.Page) -> list[str]:
    """
    Extract table from a pdfplumber page and convert it into markdown-like text.
    """
    tables_text: list[str] = []

    try:
        tables = page.extract_tables()
    except Exception:
        return tables_text

    for table_idx, table in enumerate(tables):
        if not table:
            continue

        cleaned_rows = []
        for row in table:
            cleaned_row = [
                str(cell).replace("\n", " ").strip() if cell is not None else ""
                for cell in row
            ]
            cleaned_rows.append(cleaned_row)

        if not cleaned_rows:
            continue

        lines = [f"Table {table_idx + 1}:"]
        for row in cleaned_rows:
            lines.append(" | ".join(row))

        tables_text.append("\n".join(lines))

    return tables_text


def render_page_as_image(pdf_path: str, page_number: int, output_dir: str) -> str:
    """
    Render one PDF page as PNG image.
    page_number uses 1-based index.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)
    page = doc[page_number - 1]

    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
    image_path = output_path / f"{Path(pdf_path).stem}_page_{page_number}.png"
    pix.save(str(image_path))

    doc.close()
    return str(image_path)


def parse_pdf(pdf_path: str, image_output_dir: str) -> list[dict[str, Any]]:
    """
    Parse PDF into multimodal-ish documents:
    - text per page
    - tables per page
    - rendered page image path as metadata

    For this first version, chart/infographic content is handled through:
    1. parsed text if available
    2. table extraction if available
    3. page image saved for future vision captioning
    """
    parsed_docs: list[dict[str, Any]] = []

    with pdfplumber.open(pdf_path) as pdf:
        for idx, page in enumerate(pdf.pages):
            page_number = idx + 1
            source_file = Path(pdf_path).name

            text = page.extract_text() or ""
            text = text.strip()

            image_path = render_page_as_image(
                pdf_path=pdf_path,
                page_number=page_number,
                output_dir=image_output_dir,
            )

            if text:
                parsed_docs.append(
                    {
                        "content": text,
                        "metadata": {
                            "source_file": source_file,
                            "page": page_number,
                            "content_type": "text",
                            "image_path": image_path,
                        },
                    }
                )

            tables_text = extract_tables_from_page(page)

            for table_idx, table_text in enumerate(tables_text):
                parsed_docs.append(
                    {
                        "content": table_text,
                        "metadata": {
                            "source_file": source_file,
                            "page": page_number,
                            "content_type": "table",
                            "table_index": table_idx + 1,
                            "image_path": image_path,
                        },
                    }
                )

            # Tambahan dokumen visual placeholder.
            # Ini membantu metadata halaman gambar/charts tetap masuk ke knowledge base.
            parsed_docs.append(
                {
                    "content": (
                        f"Halaman {page_number} dari dokumen {source_file} memiliki representasi visual "
                        f"yang disimpan di {image_path}. Jika halaman ini berisi chart, tabel visual, "
                        f"atau infografis, gunakan metadata halaman ini untuk debugging retrieval."
                    ),
                    "metadata": {
                        "source_file": source_file,
                        "page": page_number,
                        "content_type": "page_image",
                        "image_path": image_path,
                    },
                }
            )

    return parsed_docs