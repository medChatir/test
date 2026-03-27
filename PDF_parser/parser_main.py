import os
import json
import sys
from loguru import logger

from extract_pymupdf import extract_text_pymupdf, get_pdf_metadata
from extract_pdfplumber import extract_tables_pdfplumber
from merge_outputs import merge_parser_outputs
from save_output import save_json


def parse_pdf(pdf_path: str, save: bool = True) -> dict:
    if not os.path.exists(pdf_path):
        logger.error(f"Fichier introuvable : {pdf_path}")
        return {}

    logger.info(f"=== Début parsing : {pdf_path} ===")

    pymupdf_pages = extract_text_pymupdf(pdf_path)
    metadata = get_pdf_metadata(pdf_path)
    pdfplumber_pages = extract_tables_pdfplumber(pdf_path)
    result = merge_parser_outputs(pymupdf_pages, pdfplumber_pages, pdf_path)
    result["metadata"] = metadata

    if save:
        output_path = save_json(result, pdf_path)
        logger.success(f"JSON sauvegardé : {output_path}")

    logger.success(f"=== Parsing terminé : {result['page_count']} pages ===")
    return result


def parse_directory(input_dir: str) -> list:
    pdfs = [f for f in os.listdir(input_dir) if f.endswith(".pdf")]
    return [parse_pdf(os.path.join(input_dir, f)) for f in pdfs]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage : python parser_main.py document.pdf")
        sys.exit(1)
    out = parse_pdf(sys.argv[1])
    print(json.dumps(out, indent=2, ensure_ascii=False))