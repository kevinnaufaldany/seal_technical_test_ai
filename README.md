# SEAL Technical Test — AI Engineer Intern

**Kevin Naufal Dany** | Fresh Graduate in Informatics Engineering | Institut Teknologi Sumatera

This repository contains submissions for the **AI Engineer Intern Technical Test at SEAL**.

---

## 📹 Demo & Documentation

- **Demo Video**: [YouTube Link](https://drive.google.com/...)
- **Technical Test**: [Google Drive Link](https://drive.google.com/file/d/14s4mxzA7LyiG2X2BloVRfzTPmGNFzDpc/view)

---

## 📁 Repository Structure

```
seal_technical_test/
├── 1.rag_bank_mandiri/          # Multimodal RAG for Financial Reports
├── 2.cv_slide_to_html/          # OCR Slide to Editable HTML
└── README.md
```

---

## 🔍 Task 1: Multimodal RAG for Financial Report Analysis

**Retrieval-Augmented Generation system for answering questions about financial documents.**

### Features
- PDF upload and processing
- Text & table extraction
- Visual knowledge integration (charts, infographics)
- Vector database retrieval (ChromaDB)
- LLM-powered answer generation with source citations

### Tech Stack
Python • FastAPI • LangChain • ChromaDB • Ollama • EasyOCR

### Quick Start
```bash
cd rag_bank_mandiri
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Then visit: `http://127.0.0.1:8000/docs`

---

## 🖼️ Task 2: Layout-Aware OCR Slide to Editable HTML

**Computer vision pipeline to convert slide images into editable HTML.**

### Features
- OCR text detection with bounding boxes
- Style extraction (font size, color, alignment)
- Background inpainting (text removal)
- Absolute-positioned HTML generation
- JSON metadata output

### Tech Stack
Python • EasyOCR • PyTorch • CUDA • OpenCV • NumPy

### Quick Start
```bash
cd cv_slide_to_html
pip install -r requirements.txt
python main.py
```
Output: `output/html/` — editable HTML slides

---

## 📝 License

Technical test submission for SEAL AI Engineer Intern position.
