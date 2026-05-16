import json
from pathlib import Path

import cv2
import torch

from app.config import (
    INPUT_DIR,
    JSON_DIR,
    DEBUG_DIR,
    HTML_DIR,
    BACKGROUND_DIR,
    SUPPORTED_EXTENSIONS,
)
from app.ocr import extract_text_blocks, draw_debug_boxes, extract_top_right_logo_block, get_reader
from app.postprocess import filter_noise_blocks, merge_text_blocks
from app.style_extractor import enrich_text_blocks_with_style
from app.background import remove_text_from_background
from app.html_generator import generate_html_for_slide


def print_device_info():
    print("=" * 60)
    print("DEVICE INFO")
    print("=" * 60)
    print(f"PyTorch version : {torch.__version__}")
    print(f"CUDA available  : {torch.cuda.is_available()}")
    print(f"CUDA version    : {torch.version.cuda}")

    if torch.cuda.is_available():
        print(f"GPU device      : {torch.cuda.get_device_name(0)}")
    else:
        print("GPU device      : Not detected")

    print("=" * 60)


def get_image_paths():
    image_paths = [
        path for path in INPUT_DIR.iterdir()
        if path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]
    return sorted(image_paths, key=lambda path: path.name)


def save_json(data, output_path: Path):
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    print_device_info()

    image_paths = get_image_paths()

    if not image_paths:
        print(f"Tidak ada gambar di folder: {INPUT_DIR}")
        return

    for image_path in image_paths:
        print(f"\nProcessing: {image_path.name}")

        try:
            image = cv2.imread(str(image_path))
            if image is None:
                raise ValueError(f"Failed to read image: {image_path}")

            image_height, image_width = image.shape[:2]

            # 1. OCR mentah
            raw_blocks = extract_text_blocks(str(image_path))

            # fallback OCR khusus area logo kanan atas
            raw_blocks = extract_top_right_logo_block(
                str(image_path),
                get_reader(),
                raw_blocks,
            )

            # 2. Filter noise
            filtered_blocks = filter_noise_blocks(
                raw_blocks,
                image_width=image_width,
                image_height=image_height,
            )

            # 3. Merge block paragraf / multiline
            merged_blocks = merge_text_blocks(filtered_blocks)

            # 4. Style extraction
            styled_blocks = enrich_text_blocks_with_style(
                image_path=str(image_path),
                text_blocks=merged_blocks,
            )

            # 5. Save JSON final
            json_path = JSON_DIR / f"{image_path.stem}.json"
            save_json(styled_blocks, json_path)

            # 6. Debug boxes final
            debug_path = DEBUG_DIR / f"{image_path.stem}_debug.jpg"
            draw_debug_boxes(
                image_path=str(image_path),
                text_blocks=styled_blocks,
                output_path=str(debug_path),
            )

            # 7. Background clean (hapus teks saja)
            background_path = BACKGROUND_DIR / f"{image_path.stem}_bg_clean.png"
            mask_path = DEBUG_DIR / f"{image_path.stem}_mask.png"
            remove_text_from_background(
                image_path=str(image_path),
                text_blocks=styled_blocks,
                output_background_path=str(background_path),
                output_mask_path=str(mask_path),
            )

            # 8. Generate HTML dengan background bersih
            html_path = HTML_DIR / f"{image_path.stem}.html"
            generate_html_for_slide(
                image_path=str(image_path),
                text_blocks=styled_blocks,
                output_html_path=str(html_path),
                background_image_path=str(background_path),
                editable=True,
            )

            print(f"  Raw OCR blocks     : {len(raw_blocks)}")
            print(f"  Filtered blocks    : {len(filtered_blocks)}")
            print(f"  Merged blocks      : {len(merged_blocks)}")
            print(f"  JSON saved         : {json_path}")
            print(f"  Debug image saved  : {debug_path}")
            print(f"  Mask saved         : {mask_path}")
            print(f"  Clean bg saved     : {background_path}")
            print(f"  HTML saved         : {html_path}")

        except Exception as error:
            print(f"  ERROR processing {image_path.name}: {error}")


if __name__ == "__main__":
    main()