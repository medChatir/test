import pdfplumber
from typing import List, Dict
from loguru import logger


def extract_tables_pdfplumber(pdf_path: str) -> List[Dict]:
    pages_tables = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                tables = page.extract_tables()
                cleaned_tables = [clean_table(t) for t in tables if t]
                cleaned_tables = [t for t in cleaned_tables if t]
                pages_tables.append({
                    "page_number": page_num + 1,
                    "tables": cleaned_tables,
                    "table_count": len(cleaned_tables),
                })
        return pages_tables

    except Exception as e:
        logger.error(f"Erreur pdfplumber : {e}")
        return []


def clean_table(table: List) -> List[List[str]]:
    cleaned = []
    for row in table:
        clean_row = []
        for cell in row:
            if cell is None:
                clean_row.append("")
            else:
                clean_row.append(str(cell).strip().replace("\n", " "))
        if any(c for c in clean_row):
            cleaned.append(clean_row)
    return cleaned


def table_to_dict(table: List[List[str]]) -> List[Dict]:
    if not table or len(table) < 2:
        return []
    headers = [h.lower().strip() for h in table[0]]
    return [
        {headers[i]: row[i] if i < len(row) else "" for i in range(len(headers))}
        for row in table[1:]
    ]


def detect_shareholder_table(table: List[List[str]]) -> bool:
    if not table or not table[0]:
        return False
    keywords = ["associe", "actionnaire", "part", "action", "%", "capital"]
    header_text = " ".join(str(h).lower() for h in table[0])
    return any(kw in header_text for kw in keywords)