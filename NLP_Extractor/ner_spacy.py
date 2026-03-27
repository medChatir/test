import spacy
from typing import List, Dict
from config import SPACY_MODEL, PERSON_LABELS, ORG_LABELS

nlp = None


def load_model():
    global nlp
    if nlp is None:
        nlp = spacy.load(SPACY_MODEL)
    return nlp


def extract_entities(chunk: Dict) -> Dict:
    model = load_model()
    doc = model(chunk["text"])
    persons = []
    orgs = []

    for ent in doc.ents:
        entity = {
            "text": ent.text.strip(),
            "start": ent.start_char,
            "end": ent.end_char,
            "page": chunk["page"],
            "chunk_id": chunk["chunk_id"],
            "source": "spacy",
        }
        if ent.label_ in PERSON_LABELS:
            persons.append(entity)
        elif ent.label_ in ORG_LABELS:
            orgs.append(entity)

    return {
        "page": chunk["page"],
        "chunk_id": chunk["chunk_id"],
        "persons": persons,
        "organizations": orgs,
    }


def run_ner(chunks: List[Dict]) -> List[Dict]:
    results = []
    for chunk in chunks:
        if chunk.get("text", "").strip():
            results.append(extract_entities(chunk))
    return results