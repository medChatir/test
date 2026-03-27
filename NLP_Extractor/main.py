import json
import os
import sys
from datetime import datetime

from prepare_for_nlp import prepare_document
from ner_spacy import run_ner
from llm_extractor import extract_with_llm
from entity_resolution import resolve_entities
from confidence_score import score_all_entities


def save_final_output(data: dict, output_dir: str = "data/output") -> str:
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_dir, f"final_output_{timestamp}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return output_path


def run_pipeline(parser_output: dict, use_llm: bool = True) -> dict:
    print("[1/6] Préparation des chunks...")
    chunks = prepare_document(parser_output)

    print("[2/6] NER avec spaCy...")
    ner_results = run_ner(chunks)

    all_persons = []
    all_orgs = []
    all_relations = []

    for result in ner_results:
        for p in result["persons"]:
            all_persons.append({
                "name": p["text"],
                "page": p["page"],
                "source": "spacy",
                "sources": ["spacy"],
                "chunk_id": p["chunk_id"],
            })
        for o in result["organizations"]:
            all_orgs.append({
                "name": o["text"],
                "page": o["page"],
                "source": "spacy",
                "sources": ["spacy"],
                "chunk_id": o["chunk_id"],
            })

    if use_llm:
        print("[3/6] Enrichissement Gemini...")
        for chunk in chunks:
            spacy_p = [p["name"] for p in all_persons if p.get("chunk_id") == chunk["chunk_id"]]
            spacy_o = [o["name"] for o in all_orgs if o.get("chunk_id") == chunk["chunk_id"]]
            llm_result = extract_with_llm(chunk["text"], spacy_p, spacy_o)

            for p in llm_result.get("persons", []):
                all_persons.append({
                    "name": p.get("name", ""),
                    "page": chunk["page"],
                    "source": "llm",
                    "sources": ["llm"],
                })
            for o in llm_result.get("organizations", []):
                all_orgs.append({
                    "name": o.get("name", ""),
                    "page": chunk["page"],
                    "source": "llm",
                    "sources": ["llm"],
                })
            all_relations.extend(llm_result.get("relations", []))

    print("[4/6] Résolution des entités...")
    resolved = resolve_entities(all_persons, all_orgs)

    print("[5/6] Calcul des scores...")
    resolved["persons"] = score_all_entities(resolved["persons"])
    resolved["organizations"] = score_all_entities(resolved["organizations"])

    final_output = {
        "document": parser_output.get("file_name", "unknown"),
        "entities": {
            "persons": resolved["persons"],
            "organizations": resolved["organizations"],
        },
        "relations": all_relations,
    }

    print("[6/6] Sauvegarde...")
    path = save_final_output(final_output)
    print(f"Résultat sauvegardé : {path}")
    return final_output


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage : python main.py parser_output.json")
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as f:
        parser_output = json.load(f)
    result = run_pipeline(parser_output)
    print(json.dumps(result, indent=2, ensure_ascii=False))
