from pathlib import Path

import cv2
import numpy as np


def should_skip_mask_for_block(block: dict) -> bool:
    """
    Jangan hapus PIS/logo dari background.
    Fokus utama: OCR item-nya bagus dulu.
    """
    text = str(block.get("text", "")).strip().lower()

    if text == "pis":
        return True

    return False


def create_text_mask(
    image_shape,
    text_blocks: list[dict],
    expand_x: int = 8,
    expand_y: int = 6,
):
    h, w = image_shape[:2]
    mask = np.zeros((h, w), dtype=np.uint8)

    for block in text_blocks:
        if should_skip_mask_for_block(block):
            continue

        bbox = block["bbox"]

        x = int(bbox["x"])
        y = int(bbox["y"])
        bw = int(bbox["width"])
        bh = int(bbox["height"])

        x1 = max(0, x - expand_x)
        y1 = max(0, y - expand_y)
        x2 = min(w, x + bw + expand_x)
        y2 = min(h, y + bh + expand_y)

        cv2.rectangle(mask, (x1, y1), (x2, y2), 255, thickness=-1)

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