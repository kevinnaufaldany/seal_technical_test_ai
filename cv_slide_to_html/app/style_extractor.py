from collections import Counter

import cv2
import numpy as np


def clamp(value: int, min_value: int, max_value: int) -> int:
    return max(min_value, min(value, max_value))


def rgb_to_css(rgb: tuple[int, int, int]) -> str:
    r, g, b = rgb
    return f"rgb({r}, {g}, {b})"


def get_crop(image: np.ndarray, bbox: dict, padding: int = 0) -> np.ndarray:
    h, w = image.shape[:2]

    x1 = clamp(int(bbox["x"]) - padding, 0, w - 1)
    y1 = clamp(int(bbox["y"]) - padding, 0, h - 1)
    x2 = clamp(int(bbox["x"] + bbox["width"]) + padding, 0, w)
    y2 = clamp(int(bbox["y"] + bbox["height"]) + padding, 0, h)

    return image[y1:y2, x1:x2]


def get_luminance(rgb_pixels: np.ndarray) -> np.ndarray:
    """
    Luminance standard untuk RGB.
    """
    r = rgb_pixels[:, 0].astype(np.float32)
    g = rgb_pixels[:, 1].astype(np.float32)
    b = rgb_pixels[:, 2].astype(np.float32)

    return 0.299 * r + 0.587 * g + 0.114 * b


def dominant_color_from_pixels(pixels: np.ndarray) -> tuple[int, int, int]:
    if pixels is None or len(pixels) == 0:
        return (0, 0, 0)

    # Quantize agar noise berkurang
    quantized = (pixels // 16) * 16
    tuples = [tuple(map(int, pixel)) for pixel in quantized]

    most_common = Counter(tuples).most_common(1)[0][0]

    return tuple(min(channel + 8, 255) for channel in most_common)


def estimate_background_color(image_bgr: np.ndarray, bbox: dict) -> tuple[int, int, int]:
    """
    Background diambil dari area sekitar bbox.
    Untuk teks, background biasanya warna yang paling dominan.
    """
    crop_bgr = get_crop(image_bgr, bbox, padding=10)

    if crop_bgr.size == 0:
        return (255, 255, 255)

    crop_rgb = cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2RGB)
    pixels = crop_rgb.reshape(-1, 3)

    return dominant_color_from_pixels(pixels)


def estimate_text_color(image_bgr: np.ndarray, bbox: dict) -> tuple[int, int, int]:
    """
    Estimasi warna teks yang lebih aman.

    Logika:
    - Jika background dominan gelap, teks biasanya putih.
    - Jika background dominan terang, teks biasanya hitam/biru tua.
    - Hindari memilih pixel putih background sebagai warna teks.
    """
    crop_bgr = get_crop(image_bgr, bbox, padding=2)

    if crop_bgr.size == 0:
        return (0, 0, 0)

    crop_rgb = cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2RGB)
    pixels = crop_rgb.reshape(-1, 3)

    luminance = get_luminance(pixels)
    bg_rgb = estimate_background_color(image_bgr, bbox)
    bg_lum = 0.299 * bg_rgb[0] + 0.587 * bg_rgb[1] + 0.114 * bg_rgb[2]

    # Kasus header/card biru gelap: teks putih
    if bg_lum < 120:
        light_pixels = pixels[luminance > 180]
        if len(light_pixels) > 20:
            return dominant_color_from_pixels(light_pixels)

        return (255, 255, 255)

    # Kasus background terang: cari pixel teks gelap/biru/hitam
    # Jangan ambil background putih.
    dark_pixels = pixels[luminance < 170]

    if len(dark_pixels) > 20:
        return dominant_color_from_pixels(dark_pixels)

    # Fallback untuk background terang
    return (20, 30, 40)


def estimate_font_size(bbox: dict) -> int:
    height = int(bbox["height"])
    font_size = int(height * 0.72)

    if font_size < 10:
        font_size = 10

    if font_size > 110:
        font_size = 110

    return font_size


def estimate_font_weight(bbox: dict, text: str) -> str:
    h = int(bbox["height"])
    text_len = len(text)

    if h >= 110:
        return "700"

    if text_len <= 28 and h >= 70:
        return "700"

    return "400"


def fix_text_color_by_context(block: dict, estimated_color: tuple[int, int, int], bg_color: tuple[int, int, int]) -> tuple[int, int, int]:
    """
    Rule tambahan agar teks tidak invisible.
    """
    text = block["text"].lower()
    bbox = block["bbox"]

    bg_lum = 0.299 * bg_color[0] + 0.587 * bg_color[1] + 0.114 * bg_color[2]
    color_lum = 0.299 * estimated_color[0] + 0.587 * estimated_color[1] + 0.114 * estimated_color[2]

    # Kalau background terang dan warna teks juga terang, paksa jadi hitam/biru gelap
    if bg_lum > 180 and color_lum > 180:
        return (20, 30, 40)

    # Kalau background gelap dan warna teks gelap, paksa jadi putih
    if bg_lum < 120 and color_lum < 120:
        return (255, 255, 255)

    # Header card biasanya putih
    if text in ["talent development", "cyber security", "cloud computing"]:
        return (255, 255, 255)

    # Judul besar biasanya biru
    if "portofolio layanan utama" in text:
        return (0, 94, 158)

    if "tentang perusahaan" in text:
        return (0, 94, 158)

    if "jangkauan pasar" in text:
        return (0, 94, 158)

    if "ekosistem inovasi" in text:
        return (0, 94, 158)

    return estimated_color

def estimate_text_align(block: dict) -> str:
    text = str(block["text"]).strip().lower()

    if text == "pis":
        return "left"

    if "\n" in block["text"]:
        return "center"

    return "left"


def apply_style_overrides(block: dict, style: dict) -> dict:
    text = " ".join(str(block["text"]).strip().lower().split())

    if text == "pis":
        bbox = block["bbox"]
        logo_h = int(bbox["height"])
        logo_w = int(bbox["width"])

        # lebih konservatif supaya tidak meledak
        style["font_size"] = max(34, min(58, int(logo_h * 0.42)))
        style["font_weight"] = "700"
        style["color"] = "rgb(0, 132, 224)"
        style["text_align"] = "left"
        style["background_color"] = "transparent"
        style["font_family"] = "Arial, sans-serif"
        style["line_height"] = 1.0
        style["letter_spacing"] = "0px"
        style["white_space"] = "nowrap"

    elif "portofolio layanan utama" in text:
        style["font_size"] = max(style["font_size"], 110)
        style["font_weight"] = "700"
        style["color"] = "rgb(0, 94, 158)"
        style["text_align"] = "left"

    elif "tentang perusahaan" in text:
        style["font_size"] = max(style["font_size"], 110)
        style["font_weight"] = "700"
        style["color"] = "rgb(0, 94, 158)"
        style["text_align"] = "left"

    elif "ekosistem inovasi terintegrasi" in text:
        style["font_size"] = max(style["font_size"], 110)
        style["font_weight"] = "700"
        style["color"] = "rgb(0, 94, 158)"
        style["text_align"] = "left"

    elif "jangkauan pasar dan kontak" in text:
        style["font_size"] = max(style["font_size"], 110)
        style["font_weight"] = "700"
        style["color"] = "rgb(0, 94, 158)"
        style["text_align"] = "left"

    elif text in {"talent development", "cyber security", "cloud computing"}:
        style["font_weight"] = "700"
        style["color"] = "rgb(255, 255, 255)"
        style["text_align"] = "left"

    return style

def enrich_text_blocks_with_style(image_path: str, text_blocks: list[dict]) -> list[dict]:
    image_bgr = cv2.imread(image_path)

    if image_bgr is None:
        raise ValueError(f"Failed to read image: {image_path}")

    styled_blocks = []

    for block in text_blocks:
        bbox = block["bbox"]
        text = block["text"]

        bg_color = estimate_background_color(image_bgr, bbox)
        text_color = estimate_text_color(image_bgr, bbox)
        text_color = fix_text_color_by_context(block, text_color, bg_color)

        text_align = "left"
        if "\n" in text:
            text_align = "center"

        style = {
            "font_size": estimate_font_size(bbox),
            "font_weight": estimate_font_weight(bbox, text),
            "color": rgb_to_css(text_color),
            "background_color": rgb_to_css(bg_color),
            "font_family": "Arial, sans-serif",
            "text_align": estimate_text_align(block),
            "line_height": 1.18,
        }

        style = apply_style_overrides(block, style)

        styled_blocks.append(
            {
                **block,
                "style": style,
            }
        )

    return styled_blocks