from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_DIR = BASE_DIR / "input_slides"
OUTPUT_DIR = BASE_DIR / "output"

HTML_DIR = OUTPUT_DIR / "html"
JSON_DIR = OUTPUT_DIR / "json"
BACKGROUND_DIR = OUTPUT_DIR / "backgrounds"
DEBUG_DIR = OUTPUT_DIR / "debug"

SUPPORTED_EXTENSIONS = [".jpg", ".jpeg", ".png"]

for folder in [INPUT_DIR, OUTPUT_DIR, HTML_DIR, JSON_DIR, BACKGROUND_DIR, DEBUG_DIR]:
    folder.mkdir(parents=True, exist_ok=True)