import os
import json
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Manually set path to tesseract.exe if not auto-detected
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Base directories (relative to project root)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW_FOLDER = os.path.join(BASE_DIR, "data", "raw")
CLEAN_FOLDER = os.path.join(BASE_DIR, "data", "cleaned")
OUTPUT_FILE = os.path.join(CLEAN_FOLDER, "chunks.json")

os.makedirs(CLEAN_FOLDER, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    """Extract text from normal or scanned PDFs with page tracking."""
    pages_text = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages, start=1):
                page_text = page.extract_text()
                if page_text and page_text.strip():
                    pages_text.append({"page": i, "text": page_text})
                else:
                    # OCR fallback with reduced DPI for performance
                    images = convert_from_path(pdf_path, first_page=i, last_page=i, dpi=200)
                    ocr_text = pytesseract.image_to_string(images[0])
                    if ocr_text.strip():
                        pages_text.append({"page": i, "text": ocr_text})
    except Exception as e:
        print(f"❌ Error reading {pdf_path}: {e}")
    return pages_text

def extract_text_from_txt(txt_path):
    """Read plain text files."""
    try:
        with open(txt_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read().strip()
            return [{"page": 1, "text": content}] if content else []
    except Exception as e:
        print(f"❌ Error reading {txt_path}: {e}")
        return []

def chunk_text(text, chunk_size=800, overlap=100):
    """Split text into smaller chunks for embeddings."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    return splitter.split_text(text)

def main():
    all_chunks = []
    for file in os.listdir(RAW_FOLDER):
        file_path = os.path.join(RAW_FOLDER, file)

        if file.lower().endswith(".pdf"):
            print(f"📄 Processing PDF: {file}")
            pages = extract_text_from_pdf(file_path)

        elif file.lower().endswith(".txt"):
            print(f"📜 Processing TXT: {file}")
            pages = extract_text_from_txt(file_path)

        else:
            print(f"⚠️ Skipping unsupported file: {file}")
            continue

        if not pages:
            print(f"⚠️ No text extracted from {file}, skipping...")
            continue

        for page_data in pages:
            page_num = page_data["page"]
            text = page_data["text"].replace("\n", " ").strip()
            if not text:
                continue
            chunks = chunk_text(text)
            for i, chunk in enumerate(chunks):
                all_chunks.append({
                    "source": file,
                    "page": page_num,
                    "chunk": i,
                    "text": chunk
                })

    if all_chunks:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(all_chunks, f, ensure_ascii=False, indent=2)
        print(f"✅ Saved {len(all_chunks)} chunks to {OUTPUT_FILE}")
    else:
        print("⚠️ No chunks generated. Check your input files.")

if __name__ == "__main__":
    main()
