import re
from typing import List, Dict


def clean_text(text: str) -> str:
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)
    text = re.sub(r" {2,}", " ", text)
    text = re.sub(r"[-–]\s*\d+\s*[-–]", "", text)
    text = re.sub(r"Page\s+\d+\s*/\s*\d+", "", text)
    text = text.replace("\u2019", "'")
    return text.strip()


def split_into_chunks(text: str, max_words: int = 300) -> List[str]:
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = []
    current_words = 0

    for para in paragraphs:
        words = para.split()
        if current_words + len(words) > max_words:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
            current_chunk = words
            current_words = len(words)
        else:
            current_chunk.extend(words)
            current_words += len(words)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def prepare_document(parser_output: dict) -> List[Dict]:
    result = []
    for page in parser_output.get("pages", []):
        page_num = page["page_number"]
        text = clean_text(page.get("text", ""))
        chunks = split_into_chunks(text)
        for i, chunk in enumerate(chunks):
            result.append({
                "page": page_num,
                "chunk_id": f"p{page_num}_c{i}",
                "text": chunk,
                "tables": page.get("tables", []),
            })
    return result