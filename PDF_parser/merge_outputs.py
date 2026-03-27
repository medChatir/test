from typing import Dict
from clean_text import clean_text
from extract_pdfplumber import detect_shareholder_table, table_to_dict


def merge_parser_outputs(pymupdf_pages, pdfplumber_pages, pdf_path) -> Dict:
    tables_by_page = {
        p["page_number"]: p["tables"]
        for p in pdfplumber_pages
    }

    merged_pages = []

    for page in pymupdf_pages:
        page_num = page["page_number"]
        clean = clean_text(page.get("text", ""))
        tables = tables_by_page.get(page_num, [])

        shareholder_tables = [
            table_to_dict(t)
            for t in tables
            if detect_shareholder_table(t)
        ]

        merged_pages.append({
            "page_number": page_num,
            "text": clean,
            "raw_text": page.get("text", ""),
            "tables": tables,
            "shareholder_tables": shareholder_tables,
            "source": page.get("source", "digital"),
            "has_tables": len(tables) > 0,
        })

    return {
        "file_name": pdf_path,
        "page_count": len(merged_pages),
        "pages": merged_pages,
    }