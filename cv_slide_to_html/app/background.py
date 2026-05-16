from pathlib import Path

import cv2
import numpy as np


def normalize_text(text: str) -> str:
    return str(text).strip().lower()


def is_pis_block(block: dict) -> bool:
    text = normalize_text(block.get("text", ""))

    return text in {
        # "pis",
        "qfpis",
        "qpis",
        "ofpis",
        "pıs",
    }


def get_mask_bbox_from_block(block: dict, expand_x: int = 8, expand_y: int = 6):
    """
    Ambil koordinat mask dari raw_points kalau ada.
    Kalau raw_points kosong, pakai bbox.
    """
    raw_points = block.get("raw_points", [])

    if raw_points and len(raw_points) >= 4:
        xs = [int(p[0]) for p in raw_points]
        ys = [int(p[1]) for p in raw_points]

        x1 = min(xs) - expand_x
        y1 = min(ys) - expand_y
        x2 = max(xs) + expand_x
        y2 = max(ys) + expand_y

        return x1, y1, x2, y2

    bbox = block["bbox"]

    x = int(bbox["x"])
    y = int(bbox["y"])
    w = int(bbox["width"])
    h = int(bbox["height"])

    x1 = x - expand_x
    y1 = y - expand_y
    x2 = x + w + expand_x
    y2 = y + h + expand_y

    return x1, y1, x2, y2


def create_text_mask(
    image_shape,
    text_blocks: list[dict],
    expand_x: int = 8,
    expand_y: int = 6,
):
    h, w = image_shape[:2]
    mask = np.zeros((h, w), dtype=np.uint8)

    for block in text_blocks:
        text = normalize_text(block.get("text", ""))

        # PIS tetap ikut mask.
        # Jangan ada continue untuk pis di sini.
        x1, y1, x2, y2 = get_mask_bbox_from_block(
            block,
            expand_x=expand_x,
            expand_y=expand_y,
        )

        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(w, x2)
        y2 = min(h, y2)

        cv2.rectangle(
            mask,
            (x1, y1),
            (x2, y2),
            255,
            thickness=-1,
        )

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    mask = cv2.dilate(mask, kernel, iterations=1)

    return mask


def remove_text_from_background(
    image_path: str,
    text_blocks: list[dict],
    output_background_path: str,
    output_mask_path: str | None = None,
):
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError(f"Failed to read image: {image_path}")

    mask = create_text_mask(image.shape, text_blocks)

    clean_background = cv2.inpaint(
        image,
        mask,
        inpaintRadius=5,
        flags=cv2.INPAINT_TELEA,
    )

    output_background_path = str(output_background_path)
    Path(output_background_path).parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(output_background_path, clean_background)

    if output_mask_path:
        output_mask_path = str(output_mask_path)
        Path(output_mask_path).parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(output_mask_path, mask)

    return output_background_path