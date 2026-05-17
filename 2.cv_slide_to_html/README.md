# CV Slide to Editable HTML - OCR & Computer Vision System

A Computer Vision + OCR system that converts static presentation slides (JPG/PNG) into editable HTML pages while preserving the original visual layout and design.

## 📋 Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Pipeline Stages](#pipeline-stages)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Output Files](#output-files)
- [Troubleshooting](#troubleshooting)
- [Demo Narration](#demo-narration)

---

## 🎯 Overview

CV Slide to HTML is an automated pipeline that transforms presentation slide images into interactive, editable HTML pages. The system uses Computer Vision and OCR technologies to extract text, detect its properties, remove text from the background, and reconstruct the slide as an editable web document.

### Key Features

- ✅ **OCR Text Detection** - Accurately extract text from slide images using EasyOCR
- ✅ **Intelligent Post-processing** - Clean OCR results, filter noise, merge multiline text
- ✅ **Style Estimation** - Automatically detect font size, color, weight, and alignment
- ✅ **Background Cleaning** - Remove original text from slides using OpenCV inpainting
- ✅ **Editable HTML Generation** - Create browser-friendly HTML with contenteditable text layers
- ✅ **GPU Acceleration** - Leverage CUDA for faster OCR processing
- ✅ **Debug Output** - Generate visualization masks and debug images for transparency
- ✅ **Batch Processing** - Process multiple slides in one pipeline run

---

## 🏗️ System Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    CV Slide to Editable HTML                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  INPUT: Slide Images (JPG/PNG)                                 │
│         ↓                                                        │
│  [Image Loader] ─────────────→ OpenCV Read                      │
│         ↓                                                        │
│  [OCR Engine] ────────────────→ EasyOCR + PyTorch + CUDA        │
│         ↓                                                        │
│  [Raw OCR Blocks]                                               │
│         ↓                                                        │
│  [Post-processor] ────────────→ Python (Normalize, Merge)       │
│         ↓                                                        │
│  [Clean OCR Blocks]                                             │
│         ↓                                                        │
│  [Style Extractor] ───────────→ Font Size, Color, Weight        │
│         ↓                                                        │
│  [Styled Text Blocks]                                           │
│         ↓                                                        │
│  [Mask Generator] ─────────────→ OpenCV + NumPy                 │
│         ↓                                                        │
│  [Text Mask]                                                    │
│         ↓                                                        │
│  [Background Cleaner] ─────────→ OpenCV Inpainting              │
│         ↓                                                        │
│  [Clean Background Image]                                       │
│         ↓                                                        │
│  [JSON Writer]                                                  │
│         ↓                                                        │
│  [HTML Generator] ────────────→ HTML + CSS + contenteditable    │
│         ↓                                                        │
│  OUTPUT: Editable HTML Slides                                   │
│          ├─ JSON Layout Files                                   │
│          ├─ Debug Images                                        │
│          ├─ Text Masks                                          │
│          └─ Clean Backgrounds                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Main Data Flow (Simplified)

```
Input Slide Image
   ↓
OCR Detection
   ↓
OCR Post-processing
   ↓
Style Extraction
   ↓
Text Mask Generation
   ↓
Background Inpainting
   ↓
HTML Rendering
   ↓
Editable HTML Output
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- NVIDIA GPU with CUDA support (optional, but recommended)
- At least 4GB RAM (8GB+ with GPU)

### Installation

```bash
# Navigate to project
cd cv_slide_to_html

# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # On Windows
# or
source venv/bin/activate      # On Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### Run the Pipeline

```bash
# Place your slide images in input_slides/ folder
# Then run the pipeline
python main.py

# Output will be generated in output/ folder
```

### Access the Output

```bash
# Generated files will be in:
output/html/           # Editable HTML files
output/json/           # OCR data and layout
output/debug/          # Debug images with bounding boxes
output/backgrounds/    # Clean background images
```

Open any generated HTML file in a browser to see and edit the slide content.

---

## 📦 Installation

### Step-by-Step Setup

#### 1. Prerequisites Installation

```bash
# Install Python dependencies
pip install -r requirements.txt
```

#### 2. Verify GPU/CUDA Setup (Optional)

```bash
# Check if PyTorch can detect GPU
python -c "import torch; print(torch.cuda.is_available())"

# If True, GPU acceleration is available
```

#### 3. Test Installation

```bash
# Verify all modules can be imported
python -c "import easyocr; import cv2; import numpy as np; print('All modules loaded successfully')"
```

#### 4. Prepare Input

Create `input_slides/` folder and add your slide images:

```bash
mkdir input_slides
# Copy your JPG/PNG files here
```

---

## 💻 Usage

### Basic Usage

```bash
# Run pipeline on all slides in input_slides/
python main.py
```

### Processing Specific Slides

```bash
# Edit main.py to specify which files to process
# Then run:
python main.py
```

### Using Configuration

Edit `app/config.py` to customize behavior:

```python
# Input/Output paths
INPUT_FOLDER = "./input_slides"
OUTPUT_FOLDER = "./output"

# OCR Settings
OCR_LANGUAGE = ['en', 'id']  # Languages to detect
OCR_GPU = True               # Use GPU if available

# Processing Settings
MERGE_MULTILINE = True
FILTER_NOISE = True
NOISE_THRESHOLD = 5          # Min text block width in pixels
```

### Output Structure

After running the pipeline, you'll have:

```
output/
├── json/
│   ├── slide_1.json
│   ├── slide_2.json
│   └── ...
├── html/
│   ├── slide_1.html
│   ├── slide_2.html
│   └── ...
├── debug/
│   ├── slide_1_debug.jpg    # With OCR bounding boxes
│   ├── slide_1_mask.png     # Text mask visualization
│   └── ...
└── backgrounds/
    ├── slide_1_bg_clean.png  # Cleaned background
    ├── slide_2_bg_clean.png
    └── ...
```

---

## 📊 Pipeline Stages

### Stage 1: Input Slide

**Input:** JPG/PNG image files in `input_slides/` folder

**Process:**
- Scan folder for image files
- Filter by extension (.jpg, .jpeg, .png)

**Output:** List of image file paths

```bash
input_slides/
├── slide_1.jpg
├── slide_2.jpg
├── slide_3.jpg
└── slide_4.jpg
```

---

### Stage 2: Image Loading

**Module:** `app/background.py` (image I/O functions)

**Technology:** OpenCV

**Process:**
1. Read image using `cv2.imread()`
2. Extract image dimensions (width, height, channels)
3. Validate image format

**Output:**
```python
{
    "image": numpy.ndarray,        # Image data
    "width": 1920,                 # Pixel width
    "height": 1080,                # Pixel height
    "filename": "slide_1.jpg"      # Original filename
}
```

---

### Stage 3: OCR Detection

**Module:** `app/ocr.py`

**Technology:** EasyOCR + PyTorch + CUDA

**Process:**
1. Initialize EasyOCR reader
2. Detect text regions in image
3. Extract text, confidence, and bounding boxes
4. Get raw points for polygon detection

**Output per text block:**
```json
{
  "text": "Talent Development",
  "bbox": {
    "x": 590,
    "y": 800,
    "width": 1000,
    "height": 120
  },
  "confidence": 0.95,
  "raw_points": [
    [590, 800],
    [1590, 800],
    [1590, 920],
    [590, 920]
  ]
}
```

**Visualization:** Debug image with bounding boxes drawn

---

### Stage 4: OCR Post-processing

**Module:** `app/postprocess.py`

**Process:**

```
Raw OCR Blocks
     ↓
Normalize Text
     ↓
Filter Noise
     ├─ Remove blocks < 5px width
     ├─ Remove single characters
     └─ Remove common noise (jr, data, etc.)
     ↓
Normalize Logo Text
     ├─ qfpis → PIS
     ├─ qpis → PIS
     └─ Similar variations
     ↓
Merge Multiline Blocks
     ├─ Group adjacent text vertically
     ├─ Combine into single block
     └─ Update bounding box
     ↓
Clean OCR Blocks
```

**Example:**

```
Raw OCR:
- "Program"
- "SEAL,"
- "Talenesia, dan"
- "Magang Hub"

After merging:
- "Program SEAL, Talenesia, dan Magang Hub"
```

**Output:** Cleaned OCR blocks ready for style extraction

---

### Stage 5: Style Extraction

**Module:** `app/style_extractor.py`

**Technology:** OpenCV + Heuristic Analysis

**Process:**

```
Clean OCR Block
     ↓
Crop Area Around Text
     ↓
Analyze Pixel Patterns
     ├─ Font Size: BBox height / text length
     ├─ Font Color: Dominant color in text area
     ├─ Font Weight: Pixel density analysis
     ├─ Alignment: BBox position in image
     └─ Background Color: Dominant background color
     ↓
Build Style Dictionary
```

**Output per block:**
```json
{
  "text": "Talent Development",
  "bbox": {
    "x": 590,
    "y": 800,
    "width": 1000,
    "height": 120
  },
  "style": {
    "font_size": 72,
    "font_weight": "700",
    "color": "rgb(255, 255, 255)",
    "font_family": "Arial, sans-serif",
    "text_align": "left"
  }
}
```

---

### Stage 6: Text Mask Generation

**Module:** `app/background.py`

**Technology:** OpenCV + NumPy

**Purpose:** Create a mask to identify text areas for removal

**Process:**

```
Styled OCR Blocks
     ↓
Create Empty Mask (black)
     ↓
For Each Text Block:
     ├─ If has raw_points → Use polygon
     ├─ Else → Use bounding box rectangle
     ├─ Draw white area on mask
     └─ Mark area as text
     ↓
Final Text Mask
(black = background, white = text)
```

**Mask Format:**
- Grayscale image (single channel)
- White (255) = text area to remove
- Black (0) = background to keep

**Visualization:** Binary mask image saved to debug folder

---

### Stage 7: Background Cleaning with Inpainting

**Module:** `app/background.py`

**Technology:** OpenCV Inpainting

**Purpose:** Remove original text from slide background

**Process:**

```
Original Slide Image + Text Mask
     ↓
OpenCV Inpainting
(cv2.inpaint with Telea algorithm)
     ↓
Reconstructed Background
(text removed, background preserved)
```

**How it works:**
- Text mask marks areas to remove
- Inpainting algorithm reconstructs pixel values
- Uses surrounding pixels to fill in text areas
- Result is a clean background without original text

**Output:** Clean background image

```
output/backgrounds/slide_1_bg_clean.png
```

---

### Stage 8: JSON Output

**Module:** `app/main.py`

**Purpose:** Save OCR data for future use

**Format:**
```json
{
  "slide_name": "slide_1",
  "width": 1920,
  "height": 1080,
  "text_blocks": [
    {
      "text": "Talent Development",
      "bbox": {
        "x": 590,
        "y": 800,
        "width": 1000,
        "height": 120
      },
      "style": {
        "font_size": 72,
        "font_weight": "700",
        "color": "rgb(255, 255, 255)",
        "font_family": "Arial, sans-serif",
        "text_align": "left"
      }
    }
  ]
}
```

**Output:** `output/json/slide_1.json`

---

### Stage 9: HTML Generation

**Module:** `app/html_generator.py`

**Technology:** HTML5 + CSS3

**Process:**

```
Clean Background Image + Styled OCR JSON
     ↓
Generate HTML Structure
     ├─ Create div container
     ├─ Set background image
     ├─ Set canvas dimensions
     └─ Apply CSS styles
     ↓
Create Text Layers
For Each Text Block:
     ├─ Create <span> element
     ├─ Apply absolute positioning
     ├─ Apply text styles
     ├─ Add contenteditable attribute
     └─ Append to container
     ↓
Generate Complete HTML Document
```

**HTML Structure:**

```html
<!DOCTYPE html>
<html>
<head>
    <title>Slide 1</title>
    <style>
        .slide-container {
            position: relative;
            width: 1920px;
            height: 1080px;
            background-image: url('slide_1_bg_clean.png');
            background-size: cover;
        }
        .text-layer {
            position: absolute;
            white-space: nowrap;
        }
    </style>
</head>
<body>
    <div class="slide-container">
        <span class="text-layer" 
              contenteditable="true"
              style="left: 590px; top: 800px; width: 1000px; 
                     font-size: 72px; color: rgb(255, 255, 255);">
            Talent Development
        </span>
        <!-- More text layers -->
    </div>
</body>
</html>
```

**Output:** `output/html/slide_1.html`

---

## 📁 Project Structure

```
cv_slide_to_html/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── main.py                           # Pipeline entry point
│
├── app/
│   ├── __init__.py
│   ├── config.py                     # Configuration and paths
│   ├── ocr.py                        # EasyOCR integration
│   ├── postprocess.py                # OCR result cleaning
│   ├── style_extractor.py            # Font style estimation
│   ├── background.py                 # Mask generation & inpainting
│   └── html_generator.py             # HTML output generation
│
├── input_slides/                      # Input directory for slide images
│   ├── slide_1.jpg
│   ├── slide_2.jpg
│   └── ...
│
└── output/
    ├── json/                         # OCR data in JSON format
    ├── html/                         # Generated HTML files
    ├── debug/                        # Visualization images
    └── backgrounds/                  # Cleaned background images
```

### File Descriptions

| File | Purpose |
|------|---------|
| `main.py` | Pipeline orchestration, manages workflow stages |
| `config.py` | Global settings: paths, language, processing parameters |
| `ocr.py` | EasyOCR initialization and text detection |
| `postprocess.py` | Noise filtering, text normalization, multiline merging |
| `style_extractor.py` | Font size, color, weight, alignment estimation |
| `background.py` | Mask generation and OpenCV inpainting for background cleanup |
| `html_generator.py` | HTML/CSS generation with contenteditable text layers |

---

## 🔧 Technology Stack

### 1. **Python 3.9+**

- **Role:** Primary programming language
- **Why:** Excellent computer vision and OCR libraries ecosystem
- **Used for:** Entire pipeline orchestration

---

### 2. **EasyOCR**

- **Role:** Optical Character Recognition (OCR)
- **What it does:** Detects and extracts text from images
- **Output:** Text content, bounding boxes, confidence scores
- **Advantages:**
  - Simple API
  - Supports GPU acceleration
  - Handles various text orientations
  - Works offline (no API needed)
- **Used in:** `app/ocr.py`

---

### 3. **PyTorch**

- **Role:** Deep learning framework (EasyOCR backend)
- **What it does:** Powers the OCR neural networks
- **GPU Support:** Automatic CUDA detection and usage
- **System Info:**
  ```
  CUDA available: True
  GPU device: NVIDIA GeForce RTX 3050 Laptop GPU
  ```

---

### 4. **CUDA / GPU**

- **Role:** Hardware acceleration
- **What it does:** Speeds up OCR inference on NVIDIA GPUs
- **Performance:** 5-10x faster than CPU
- **Your GPU:** NVIDIA GeForce RTX 3050 Laptop GPU

---

### 5. **OpenCV**

- **Role:** Computer Vision library
- **Key Functions Used:**
  - `cv2.imread()` - Read images
  - `cv2.inpaint()` - Remove text from background
  - `cv2.drawContours()` - Draw bounding boxes (debug)
  - `cv2.cvtColor()` - Color space conversion
- **Used in:** `app/background.py`, `app/ocr.py`

---

### 6. **NumPy**

- **Role:** Array manipulation and mathematical operations
- **Used for:** 
  - Mask creation and manipulation
  - Coordinate calculations
  - Pixel analysis
- **Used in:** `app/background.py`, `app/style_extractor.py`

---

### 7. **PIL / Pillow**

- **Role:** Image I/O and basic image operations
- **Used for:**
  - Image size reading
  - Thumbnail generation
  - Format conversion
- **Used in:** `app/background.py`

---

### 8. **HTML5 + CSS3**

- **Role:** Frontend markup and styling
- **Key CSS Features:**
  - `position: absolute` - Precise text positioning
  - `contenteditable` - Make text editable in browser
  - `background-image` - Display clean background
- **Used in:** `app/html_generator.py`

---

### 9. **JSON**

- **Role:** Data interchange format
- **Usage:** Store OCR results and layout data
- **Advantages:**
  - Human-readable
  - Easy to parse
  - Good for debugging
- **Used in:** `app/main.py`

---

## ⚙️ Configuration

### Default Configuration (`app/config.py`)

```python
# Folder Configuration
INPUT_FOLDER = "./input_slides"
OUTPUT_FOLDER = "./output"

# OCR Configuration
OCR_LANGUAGE = ['en', 'id']        # Languages to recognize
OCR_GPU = True                      # Use GPU acceleration
OCR_CONFIDENCE_THRESHOLD = 0.3      # Minimum confidence to keep

# Post-processing Configuration
MERGE_MULTILINE = True              # Merge adjacent text blocks
FILTER_NOISE = True                 # Remove small/invalid blocks
NOISE_THRESHOLD = 5                 # Min text block width (pixels)
LOGO_TEXT_MAPPING = {               # Normalize logo text
    'qfpis': 'PIS',
    'qpis': 'PIS',
    'pis': 'PIS'
}

# Style Extraction Configuration
ESTIMATE_FONT_SIZE = True           # Estimate text size
ESTIMATE_FONT_COLOR = True          # Detect text color
ESTIMATE_ALIGNMENT = True           # Detect text alignment

# Inpainting Configuration
INPAINT_METHOD = 'telea'            # OpenCV inpainting method
INPAINT_RADIUS = 3                  # Inpainting brush size

# Output Configuration
SAVE_DEBUG_IMAGES = True            # Save bounding box visualizations
SAVE_MASKS = True                   # Save mask images
SAVE_CLEAN_BACKGROUNDS = True       # Save inpainted backgrounds
SAVE_JSON = True                    # Save OCR JSON data
SAVE_HTML = True                    # Generate HTML files
```

### Customization Examples

#### Enable/Disable Features

```python
# In app/config.py
MERGE_MULTILINE = False      # Don't merge text blocks
FILTER_NOISE = False         # Keep all OCR results
SAVE_DEBUG_IMAGES = False    # Skip debug visualization
```

#### Adjust OCR Settings

```python
# Faster OCR (less accurate)
OCR_LANGUAGE = ['en']        # Single language
OCR_CONFIDENCE_THRESHOLD = 0.5

# More accurate OCR (slower)
OCR_LANGUAGE = ['en', 'id', 'ja']
OCR_CONFIDENCE_THRESHOLD = 0.1
```

#### Modify Processing Parameters

```python
# More aggressive noise filtering
NOISE_THRESHOLD = 20

# More text blocks merged
MERGE_MULTILINE = True

# Stronger inpainting
INPAINT_RADIUS = 5
```

---

## 📤 Output Files

### 1. JSON Output (`output/json/`)

**Format:** Structured OCR data

```json
{
  "slide_name": "slide_1",
  "width": 1920,
  "height": 1080,
  "text_blocks": [
    {
      "text": "Portofolio Layanan",
      "bbox": {
        "x": 183,
        "y": 120,
        "width": 2600,
        "height": 300
      },
      "confidence": 0.92,
      "style": {
        "font_size": 96,
        "font_weight": "700",
        "color": "rgb(255, 255, 255)",
        "font_family": "Arial, sans-serif",
        "text_align": "center"
      }
    }
  ]
}
```

**Usage:** Debugging, feeding to other systems, data preservation

---

### 2. HTML Output (`output/html/`)

**Format:** Interactive web pages with editable text

**Features:**
- Preserves original slide layout and design
- Text is fully editable with `contenteditable`
- Can be saved with new text values
- Works in all modern browsers

**How to use:**
1. Open HTML file in browser
2. Click on any text to edit
3. Make changes
4. Save the page (Ctrl+S)

---

### 3. Debug Output (`output/debug/`)

**Files Generated:**

| File | Purpose |
|------|---------|
| `slide_1_debug.jpg` | Original slide with OCR bounding boxes |
| `slide_1_mask.png` | Binary mask showing detected text areas |

**Usage:**
- Verify OCR accuracy
- Check if text regions are properly detected
- Troubleshoot occlusion or missed text
- Visualize preprocessing results

---

### 4. Background Output (`output/backgrounds/`)

**Files Generated:**

| File | Purpose |
|------|---------|
| `slide_1_bg_clean.png` | Clean background with text removed |

**Quality:**
- Text completely removed
- Background artifacts minimized
- Original design/graphics preserved
- Used as background in final HTML

---

## 🐛 Troubleshooting

### Issue: OCR Detects Very Few or No Text

**Causes:**
- Image quality too low
- Text color too similar to background
- Image size too small

**Solutions:**
```python
# Lower confidence threshold
OCR_CONFIDENCE_THRESHOLD = 0.1

# Try different languages
OCR_LANGUAGE = ['en', 'id']

# Upscale image before processing
# (modify in app/ocr.py)
scale_factor = 2
image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor)
```

---

### Issue: Out of Memory Error

**Cause:** Image too large or batch processing too many files

**Solutions:**

```python
# Reduce batch size
# Or process one image at a time

# Reduce image resolution before processing
# In app/ocr.py:
max_width = 1920
if image.shape[1] > max_width:
    scale = max_width / image.shape[1]
    image = cv2.resize(image, None, fx=scale, fy=scale)
```

---

### Issue: GPU Not Being Used

**Cause:** CUDA not properly configured or GPU out of memory

**Check GPU Status:**
```python
python -c "import torch; print('GPU available:', torch.cuda.is_available()); print('Device:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
```

**Solutions:**
```python
# Force CPU mode
OCR_GPU = False

# Or update PyTorch with correct CUDA version
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

---

### Issue: Text Mask Missing Large Text Areas

**Cause:** OCR didn't detect all text, or confidence threshold too high

**Solutions:**
```python
# Lower confidence threshold
OCR_CONFIDENCE_THRESHOLD = 0.2

# Manually inspect debug image
# Check output/debug/slide_X_debug.jpg
```

---

### Issue: Background Inpainting Produces Artifacts

**Cause:** Inpainting radius too large or image has complex patterns

**Solutions:**
```python
# Reduce inpainting radius
INPAINT_RADIUS = 2

# Try different inpainting method
INPAINT_METHOD = 'ns'  # Navier-Stokes instead of Telea
```

---

### Issue: Generated HTML Text Not Centered or Positioned Incorrectly

**Cause:** Style extraction gave wrong values

**Manual Fix in HTML:**
```html
<!-- Find the problematic span and adjust -->
<span style="left: 590px; top: 800px; font-size: 72px;">
    Text content
</span>
<!-- Change left, top, or font-size values as needed -->
```

---

### Issue: Duplicate Text or Noise Characters in Output

**Cause:** Post-processing didn't filter noise properly

**Solutions:**
```python
# Increase noise threshold
NOISE_THRESHOLD = 10

# Enable multiline merging to combine noise
MERGE_MULTILINE = True
```

---

## 📝 Demo Narration

### Complete System Explanation

> Pada task ini, saya membuat mini sistem untuk mengubah slide image menjadi editable HTML menggunakan Computer Vision dan OCR. 
>
> **Pipeline dimulai** dari input gambar slide, kemudian sistem menjalankan OCR menggunakan EasyOCR untuk mendeteksi teks beserta bounding box-nya. Proses OCR berjalan di atas PyTorch dan memanfaatkan CUDA untuk akselerasi GPU.
>
> **Hasil OCR kemudian diproses ulang** untuk menghapus noise, menormalisasi teks tertentu seperti logo, dan menggabungkan teks multiline agar lebih rapi. Tahap ini penting karena hasil OCR mentah sering berantakan dan perlu dibersihkan.
>
> **Setelah OCR bersih**, sistem melakukan estimasi style menggunakan heuristic rules berbasis OpenCV. Style yang diestimasi meliputi ukuran font, warna teks, ketebalan font, dan alignment. Informasi ini nantinya digunakan saat generate HTML.
>
> **Langkah kritis berikutnya** adalah membuat mask berdasarkan koordinat teks OCR. Mask ini adalah gambar binary yang menandai area teks dengan warna putih dan background dengan warna hitam.
>
> **Mask tersebut kemudian digunakan** pada proses OpenCV inpainting untuk menghapus teks asli dari background slide. Algoritma inpainting (Telea) merekonstruksi nilai pixel di area teks menggunakan informasi dari pixel sekitarnya, menghasilkan background yang bersih tanpa teks asli.
>
> **Terakhir**, sistem membuat HTML dengan background slide yang sudah dibersihkan sebagai background-image, lalu menambahkan teks OCR sebagai elemen HTML absolut yang bisa diedit melalui contenteditable attribute. 
>
> **Output akhirnya** berupa file JSON untuk penyimpanan data, debug image untuk visualisasi, mask untuk transparency, clean background untuk rendering, dan HTML editable yang bisa langsung dibuka di browser untuk editing.

---

## 🎓 Key Technical Concepts

### Optical Character Recognition (OCR)

- Detects text regions in images using deep neural networks
- Returns text content, confidence score, and bounding boxes
- EasyOCR uses CRAFT (text detection) + CRNN (text recognition)

### Text Masking

- Binary image where white areas mark detected text
- Used to identify regions that need to be removed
- Can use polygon (raw_points) or rectangle (bbox)

### Image Inpainting

- Reconstructs image content in specified regions
- Uses surrounding pixels to fill text areas naturally
- Telea algorithm propagates information from boundary pixels

### Style Extraction

- Estimates font properties from pixel patterns
- Font size: derived from bounding box height
- Font color: dominant color in text region
- Font weight: pixel density analysis
- Alignment: relative position in image

### Absolute Positioning in HTML

- CSS `position: absolute` places elements at exact coordinates
- Allows precise layering of text over background image
- Maintains original slide layout in web format

### Content Editability

- HTML5 `contenteditable="true"` attribute makes text editable
- Users can click and modify text in browser
- Data persists until explicitly saved

---

## 📚 References

- [EasyOCR Documentation](https://github.com/JaidedAI/EasyOCR)
- [OpenCV Documentation](https://docs.opencv.org/)
- [PyTorch Documentation](https://pytorch.org/docs/)
- [MDN Web Docs - contenteditable](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/contenteditable)
- [CSS Positioning](https://developer.mozilla.org/en-US/docs/Web/CSS/position)

---

## ✅ Verification Checklist

- [ ] Python 3.9+ installed
- [ ] Virtual environment created and activated
- [ ] `pip install -r requirements.txt` completed without errors
- [ ] GPU/CUDA verified (optional): `python -c "import torch; print(torch.cuda.is_available())"`
- [ ] `input_slides/` folder created with test images
- [ ] `python main.py` runs without errors
- [ ] `output/` folder generated with subfolders
- [ ] Debug images show correct bounding boxes in `output/debug/`
- [ ] Masks look correct in `output/debug/` (text = white)
- [ ] Clean backgrounds have text removed in `output/backgrounds/`
- [ ] JSON files contain text blocks in `output/json/`
- [ ] HTML files open in browser and text is editable in `output/html/`

---

## 📄 License

This project is part of a technical test for candidate as AI Engineer Intern in SEAL.

---

## 👤 Author

Created as a complete OCR + Computer Vision system for technical assessment.

---

## 🤝 Contributing

For improvements or enhancements:

1. Test with various slide formats and quality levels
2. Document any new parameters added to `config.py`
3. Add debug output to verify intermediate steps
4. Update this README if major functionality changes

---

**Last Updated:** May 2026  
**System Version:** 1.0  
**Status:** Production Ready  
**GPU Support:** NVIDIA CUDA available
