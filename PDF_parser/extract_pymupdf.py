import fitz
from typing import List, Dict
from loguru import logger
from config import MIN_TEXT_LENGTH, MAX_PAGES, OCR_FALLBACK


def extract_text_pymupdf(pdf_path: str) -> List[Dict]:
    pages_data = []
    try:
        doc = fitz.open(pdf_path)
        logger.info(f"PDF ouvert : {pdf_path} — {len(doc)} pages")

        for page_num in range(min(len(doc), MAX_PAGES)):
            page = doc[page_num]
            text = page.get_text("text")

            if len(text.strip()) < MIN_TEXT_LENGTH and OCR_FALLBACK:
                text = extract_ocr_fallback(page)
                source = "ocr"
            else:
                source = "digital"

            blocks = page.get_text("blocks")
            structured_blocks = [
                {
                    "text": b[4].strip(),
                    "x0": round(b[0], 1),
                    "y0": round(b[1], 1),
                    "x1": round(b[2], 1),
                    "y1": round(b[3], 1),
                    "block_type": "text" if b[6] == 0 else "image",
                }
                for b in blocks if b[4].strip()
            ]

            pages_data.append({
                "page_number": page_num + 1,
                "text": text,
                "blocks": structured_blocks,
                "source": source,
                "width": page.rect.width,
                "height": page.rect.height,
            })

        doc.close()
        return pages_data

    except Exception as e:
        logger.error(f"Erreur PyMuPDF : {e}")
        return []


def extract_ocr_fallback(page) -> str:
    try:
        import io
        import pytesseract
        from PIL import Image
        pix = page.get_pixmap(dpi=300)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        return pytesseract.image_to_string(img, lang="fra+ara")
    except Exception:
        return ""


def get_pdf_metadata(pdf_path: str) -> Dict:
    try:
        doc = fitz.open(pdf_path)
        meta = doc.metadata
        info = {
            "title": meta.get("title", ""),
            "author": meta.get("author", ""),
            "pages": len(doc),
            "encrypted": doc.is_encrypted,
        }
        doc.close()
        return info
    except Exception:
        return {}