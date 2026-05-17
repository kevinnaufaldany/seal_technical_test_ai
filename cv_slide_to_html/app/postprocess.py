import re
from typing import List


KNOWN_NOISE_WORDS = {
    "jr",
    "data",
    "9266",
    "1",
}


def normalize_text(text: str) -> str:
    return " ".join(str(text).strip().split())


def is_mostly_numeric(text: str) -> bool:
    stripped = re.sub(r"\s+", "", text)
    return stripped.isdigit()


def normalize_logo_ocr(block: dict, image_width: int, image_height: int) -> dict:
    """
    OCR-first:
    Jika EasyOCR benar-benar mendeteksi teks logo seperti qfpis/pis/qpis,
    kita normalisasi menjadi PIS.

    Catatan:
    Ini BUKAN synthetic inject.
    Kalau OCR tidak mendeteksi logo, fungsi ini tidak membuat block baru.
    """
    text = normalize_text(block.get("text", ""))
    lower = text.lower()

    bbox = block["bbox"]
    x = int(bbox["x"])
    y = int(bbox["y"])
    w = int(bbox["width"])

    is_top_right_logo_area = (
        x > image_width * 0.72
        and y < image_height * 0.20
    )

    if lower in {"qfpis", "qpis", "ofpis", "pis", "pıs"} and is_top_right_logo_area:
        # geser ke kanan agar fokus ke teks PIS, bukan ke icon
        text_x = x + int(w * 0.42)
        text_w = max(120, int(w * 0.42))

        # jaga jangan keluar canvas
        text_w = min(text_w, image_width - text_x - 8)

        block = {
            **block,
            "text": "pis",
            "bbox": {
                **bbox,
                "x": text_x,
                "width": text_w,
            },
            "confidence": max(float(block.get("confidence", 0.0)), 0.80),
            "source": "ocr_logo_normalized",
        }

    return block


def is_noise_block(block: dict, image_width: int, image_height: int) -> bool:
    text = normalize_text(block["text"])
    lower = text.lower()

    bbox = block["bbox"]
    w = int(bbox["width"])
    h = int(bbox["height"])
    area = w * h
    confidence = float(block.get("confidence", 0.0))

    if confidence < 0.30:
        return True

    if w < 18 or h < 12:
        return True

    if area < 900:
        return True

    if lower in KNOWN_NOISE_WORDS:
        return True

    if is_mostly_numeric(text) and len(text) <= 4:
        return True

    if len(text) <= 1:
        return True

    return False


def filter_noise_blocks(
    text_blocks: List[dict],
    image_width: int,
    image_height: int,
) -> List[dict]:
    filtered = []

    for block in text_blocks:
        block = normalize_logo_ocr(block, image_width, image_height)

        if is_noise_block(block, image_width, image_height):
            continue

        filtered.append(block)

    return filtered


def can_merge_blocks(prev_block: dict, curr_block: dict) -> bool:
    prev_text = normalize_text(prev_block["text"]).lower()
    curr_text = normalize_text(curr_block["text"]).lower()

    # Jangan merge PIS dengan block lain.
    if prev_text == "pis" or curr_text == "pis":
        return False

    prev_bbox = prev_block["bbox"]
    curr_bbox = curr_block["bbox"]

    prev_center_x = prev_bbox["x"] + prev_bbox["width"] / 2
    curr_center_x = curr_bbox["x"] + curr_bbox["width"] / 2

    prev_bottom = prev_bbox["y"] + prev_bbox["height"]
    curr_top = curr_bbox["y"]

    vertical_gap = curr_top - prev_bottom
    center_gap = abs(curr_center_x - prev_center_x)

    max_center_gap = max(120, min(prev_bbox["width"], curr_bbox["width"]))
    max_vertical_gap = max(18, min(prev_bbox["height"], curr_bbox["height"]) * 1.2)

    if vertical_gap < 0:
        return False

    if vertical_gap <= max_vertical_gap and center_gap <= max_center_gap:
        return True

    return False


def merge_group(group: List[dict]) -> dict:
    xs = [block["bbox"]["x"] for block in group]
    ys = [block["bbox"]["y"] for block in group]
    x2s = [block["bbox"]["x"] + block["bbox"]["width"] for block in group]
    y2s = [block["bbox"]["y"] + block["bbox"]["height"] for block in group]

    merged_text = "\n".join(normalize_text(block["text"]) for block in group)

    return {
        "text": merged_text,
        "bbox": {
            "x": min(xs),
            "y": min(ys),
            "width": max(x2s) - min(xs),
            "height": max(y2s) - min(ys),
        },
        "confidence": max(float(block.get("confidence", 0.0)) for block in group),
        "raw_points": [],
    }


def merge_text_blocks(text_blocks: List[dict]) -> List[dict]:
    if not text_blocks:
        return []

    blocks = sorted(text_blocks, key=lambda b: (b["bbox"]["y"], b["bbox"]["x"]))

    merged = []
    current_group = [blocks[0]]

    for block in blocks[1:]:
        prev_block = current_group[-1]

        if can_merge_blocks(prev_block, block):
            current_group.append(block)
        else:
            merged.append(merge_group(current_group))
            current_group = [block]

    if current_group:
        merged.append(merge_group(current_group))

    return merged