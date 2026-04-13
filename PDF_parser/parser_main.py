import argparse
import os
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
        result["output_path"] = output_path
        logger.success(f"JSON sauvegardé : {output_path}")

    logger.success(f"=== Parsing terminé : {result['page_count']} pages ===")
    return result


def parse_directory(input_dir: str) -> list:
    pdfs = [f for f in os.listdir(input_dir) if f.endswith(".pdf")]
    return [parse_pdf(os.path.join(input_dir, f)) for f in pdfs]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Parse un PDF et exporte le résultat en JSON")
    parser.add_argument("pdf_path", help="Chemin vers le PDF à parser")
    parser.add_argument(
        "--print-json",
        action="store_true",
        help="Affiche le JSON complet dans la console (désactivé par défaut)",
    )
    return parser


if __name__ == "__main__":
    args = build_parser().parse_args()
    out = parse_pdf(args.pdf_path)

    if not out:
        sys.exit(1)

    if args.print_json:
        import json

        print(json.dumps(out, indent=2, ensure_ascii=False))
    else:
        print(f"Terminé. Fichier de sortie : {out.get('output_path', 'non sauvegardé')}")
