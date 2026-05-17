from html import escape
from pathlib import Path
from PIL import Image


def css_px(value: int | float) -> str:
    return f"{int(value)}px"


def relative_path(from_file: Path, to_file: Path) -> str:
    return str(to_file.relative_to(from_file.parent.parent.parent)).replace("\\", "/")


def generate_html_for_slide(
    image_path: str,
    text_blocks: list[dict],
    output_html_path: str,
    background_image_path: str | None = None,
    editable: bool = True,
    clean_canvas_color: str = "#ffffff",
):
    image = Image.open(image_path)
    width, height = image.size

    output_path_obj = Path(output_html_path)
    output_path_obj.parent.mkdir(parents=True, exist_ok=True)

    if background_image_path:
        bg_path = Path(background_image_path)
        bg_relative = "../../output/backgrounds/" + bg_path.name
        slide_background_css = f"""
        background-image: url("{bg_relative}");
        background-size: 100% 100%;
        background-repeat: no-repeat;
        background-position: center;
        """
    else:
        slide_background_css = f"background: {clean_canvas_color};"

    text_html_parts = []

    for idx, block in enumerate(text_blocks, start=1):
        text = escape(block["text"])
        bbox = block["bbox"]
        style = block["style"]

        x = bbox["x"]
        y = bbox["y"]
        w = bbox["width"]
        h = bbox["height"]

        font_size = style["font_size"]
        color = style["color"]
        font_weight = style["font_weight"]
        font_family = style["font_family"]
        # background_color = style.get("background_color", "transparent")
        text_align = style.get("text_align", "left")
        line_height = style.get("line_height", 1.18)
        letter_spacing = style.get("letter_spacing", "0px")
        white_space = style.get("white_space", "normal")

        editable_attr = 'contenteditable="true"' if editable else ""

        text_html = f"""
        <span
          class="text-layer"
          data-index="{idx}"
          {editable_attr}
          style="
            left: {css_px(x)};
            top: {css_px(y)};
            width: {css_px(w)};
            min-height: {css_px(h)};
            font-size: {css_px(font_size)};
            color: {color};
            font-weight: {font_weight};
            font-family: {font_family};
            text-align: {text_align};
            line-height: {line_height};
            letter-spacing: {letter_spacing};
            white-space: {white_space};
          "
        >{text}</span>
        """
        text_html_parts.append(text_html)

    html = f"""<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Clean Slide HTML</title>

  <style>
    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      padding: 24px;
      background: #111827;
      font-family: Arial, sans-serif;
    }}

    .toolbar {{
      max-width: {width}px;
      margin: 0 auto 16px auto;
      color: white;
      display: flex;
      justify-content: space-between;
      gap: 12px;
    }}

    .toolbar-title {{
      font-size: 16px;
      font-weight: 700;
    }}

    .toolbar-note {{
      font-size: 13px;
      color: #d1d5db;
    }}

    .slide-wrapper {{
      width: 100%;
      overflow: auto;
    }}

    .slide {{
      position: relative;
      width: {width}px;
      height: {height}px;
      margin: 0 auto;
      {slide_background_css}
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.35);
      border-radius: 8px;
      overflow: hidden;
    }}

    .text-layer {{
      position: absolute;
      display: inline-block;
      white-space: pre-line;
      outline: none;
      z-index: 2;
      background: transparent;
    }}

    .text-layer:hover {{
      outline: 2px dashed rgba(255, 0, 0, 0.60);
      cursor: text;
    }}

    .text-layer:focus {{
      outline: 3px solid rgba(59, 130, 246, 0.9);
      background-color: rgba(255, 255, 255, 0.25);
      color: inherit;
    }}

    @media (max-width: {width}px) {{
      .slide {{
        transform: scale(calc((100vw - 48px) / {width}));
        transform-origin: top left;
        margin: 0;
      }}

      .slide-wrapper {{
        height: calc({height}px * ((100vw - 48px) / {width}));
      }}
    }}
  </style>
</head>
<body>
  <div class="toolbar">
    <div class="toolbar-title">Editable Slide HTML</div>
    <div class="toolbar-note">Background dipertahankan, hanya teks yang dibuat editable.</div>
  </div>

  <div class="slide-wrapper">
    <div class="slide">
      {''.join(text_html_parts)}
    </div>
  </div>
</body>
</html>
"""

    output_path_obj.write_text(html, encoding="utf-8")
    return output_html_path