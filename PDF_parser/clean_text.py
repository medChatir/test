import re


def clean_text(text: str) -> str:
    text = remove_page_numbers(text)
    text = fix_broken_words(text)
    text = normalize_whitespace(text)
    text = normalize_quotes(text)
    text = normalize_dashes(text)
    return text.strip()


def remove_page_numbers(text: str) -> str:
    text = re.sub(r"[-–—]\s*\d+\s*[-–—]", " ", text)
    text = re.sub(r"\bPage\s+\d+\s*[/sur]+\s*\d+\b", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^\s*\d+\s*$", "", text, flags=re.MULTILINE)
    return text


def fix_broken_words(text: str) -> str:
    text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)
    text = re.sub(r"(?<![.!?\n])\n(?![\n\-\*\d])", " ", text)
    return text


def normalize_whitespace(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def normalize_quotes(text: str) -> str:
    text = text.replace("\u2019", "'")
    text = text.replace("\u2018", "'")
    text = text.replace("\u201c", '"')
    text = text.replace("\u201d", '"')
    return text


def normalize_dashes(text: str) -> str:
    text = text.replace("\u2013", "-")
    text = text.replace("\u2014", "-")
    return text


def extract_amounts(text: str) -> dict:
    percentages = re.findall(r"(\d+(?:[.,]\d+)?)\s*%", text)
    amounts_mad = re.findall(
        r"(\d[\d\s]*(?:[.,]\d+)?)\s*(?:MAD|DH|dirhams?)",
        text,
        re.IGNORECASE,
    )
    return {
        "percentages": [float(p.replace(",", ".")) for p in percentages],
        "amounts_mad": amounts_mad,
    }