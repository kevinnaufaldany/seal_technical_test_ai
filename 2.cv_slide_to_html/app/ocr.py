import os
from typing import Any

import cv2
import easyocr
import numpy as np
import torch


_reader = None

def normalize_simple_text(text: str) -> str:
    return " ".join(str(text).strip().split()).lower()


def extract_top_right_logo_block(image_path: str, reader, existing_blocks: list[dict]) -> list[dict]:
    # kalau sudah ada PIS dari OCR utama, jangan lakukan apa-apa
    for b in existing_blocks:
        t = normalize_simple_text(b.get("text", ""))
        if t in {"pis", "qpis", "qfpis", "ofpis", "pıs"}:
            return existing_blocks

    image = cv2.imread(image_path)
    if image is None:
        return existing_blocks

    h, w = image.shape[:2]

    # crop area kanan atas
    x1 = int(w * 0.74)
    y1 = 0
    x2 = w
    y2 = int(h * 0.22)

    roi = image[y1:y2, x1:x2]
    if roi.size == 0:
        return existing_blocks

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # upscale supaya logo lebih kebaca
    scale = 3
    gray = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

    # threshold
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    results = reader.readtext(
        gray,
        detail=1,
        paragraph=False,
        allowlist="PpIiSsQqFfOo"
    )

    for points, text, conf in results:
        lower = normalize_simple_text(text)

        if lower in {"pis", "qpis", "qfpis", "ofpis", "pıs"}:
            xs = [p[0] for p in points]
            ys = [p[1] for p in points]

            rx = int(min(xs) / scale)
            ry = int(min(ys) / scale)
            rw = int((max(xs) - min(xs)) / scale)
            rh = int((max(ys) - min(ys)) / scale)

            existing_blocks.append({
                "text": "PIS",
                "bbox": {
                    "x": x1 + rx,
                    "y": y1 + ry,
                    "width": max(120, rw),
                    "height": max(30, rh),
                },
                "confidence": float(conf),
                "raw_points": [],
                "source": "ocr_logo_roi",
            })
            break

    return existing_blocks

def is_gpu_available() -> bool:
    """
    Mengecek apakah CUDA GPU tersedia untuk PyTorch/EasyOCR.
    """
    return torch.cuda.is_available()


def get_reader():
    """
    EasyOCR reader dibuat sekali saja agar tidak reload model berkali-kali.
    Jika CUDA tersedia, gunakan GPU.
    """
    global _reader

    if _reader is None:
        use_gpu = is_gpu_available()

        if use_gpu:
            print(f"[INFO] EasyOCR using GPU: {torch.cuda.get_device_name(0)}")
        else:
            print("[INFO] EasyOCR using CPU. GPU/CUDA not detected by PyTorch.")

        _reader = easyocr.Reader(
            ["id", "en"],
            gpu=use_gpu,
            verbose=False,
        )

    return _reader


def to_python_number(value: Any):
    """
    Convert numpy scalar ke tipe Python native agar aman untuk json.dump().
    """
    if isinstance(value, np.integer):
        return int(value)

    if isinstance(value, np.floating):
        return float(value)

    return value


def serialize_points(points):
    """
    Convert raw bbox points EasyOCR menjadi list Python native.
    EasyOCR kadang memberi numpy.int32, yang tidak bisa langsung di-json dump.
    """
    clean_points = []

    for point in points:
        x = int(to_python_number(point[0]))
        y = int(to_python_number(point[1]))
        clean_points.append([x, y])

    return clean_points


def normalize_bbox(points):
    clean_points = serialize_points(points)

    xs = [point[0] for point in clean_points]
    ys = [point[1] for point in clean_points]

    x_min = int(min(xs))
    y_min = int(min(ys))
    x_max = int(max(xs))
    y_max = int(max(ys))

    return {
        "x": x_min,
        "y": y_min,
        "width": int(x_max - x_min),
        "height": int(y_max - y_min),
    }


def clean_text(text: str) -> str:
    """
    Membersihkan teks OCR sederhana.
    """
    return " ".join(str(text).strip().split())


def extract_text_blocks(image_path: str, min_confidence: float = 0.25):
    """
    Extract text, bbox, confidence dari gambar.
    Output sudah JSON serializable.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    reader = get_reader()

    results = reader.readtext(
        image_path,
        detail=1,
        paragraph=False,
        contrast_ths=0.1,
        adjust_contrast=0.5,
        text_threshold=0.6,
        low_text=0.35,
        link_threshold=0.4,
    )

    text_blocks = []

    for points, text, confidence in results:
        confidence = float(to_python_number(confidence))

        if confidence < min_confidence:
            continue

        text = clean_text(text)

        if not text:
            continue

        bbox = normalize_bbox(points)
        raw_points = serialize_points(points)

        text_blocks.append(
            {
                "text": text,
                "bbox": bbox,
                "confidence": confidence,
                "raw_points": raw_points,
            }
        )

    text_blocks = sort_text_blocks(text_blocks)

    return text_blocks


def sort_text_blocks(text_blocks: list[dict]):
    """
    Urutkan teks dari atas ke bawah, kiri ke kanan.
    """
    return sorted(
        text_blocks,
        key=lambda block: (
            block["bbox"]["y"],
            block["bbox"]["x"],
        ),
    )


def draw_debug_boxes(image_path: str, text_blocks: list[dict], output_path: str):
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError(f"Failed to read image: {image_path}")

    for idx, block in enumerate(text_blocks, start=1):
        bbox = block["bbox"]
        x = int(bbox["x"])
        y = int(bbox["y"])
        w = int(bbox["width"])
        h = int(bbox["height"])

        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

        label = f"{idx}. {block['text'][:25]}"
        cv2.putText(
            image,
            label,
            (x, max(y - 8, 15)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 255),
            1,
            cv2.LINE_AA,
        )

    cv2.imwrite(output_path, image)