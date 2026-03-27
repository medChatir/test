import re
from typing import List, Dict

CIVILITY_PREFIXES = ["monsieur", "m.", "mme", "madame", "mr", "dr", "me"]
LEGAL_PREFIXES = ["societe", "la societe", "la s.a.r.l", "le groupe"]


def normalize_person(name: str) -> str:
    for prefix in CIVILITY_PREFIXES:
        pattern = re.compile(rf"^{prefix}\s+", re.IGNORECASE)
        name = pattern.sub("", name).strip()
    return name.strip().title()


def normalize_org(name: str) -> str:
    for prefix in LEGAL_PREFIXES:
        pattern = re.compile(rf"^{prefix}\s+", re.IGNORECASE)
        name = pattern.sub("", name).strip()
    return name.strip()


def deduplicate_entities(entities: List[Dict]) -> List[Dict]:
    seen = {}
    for ent in entities:
        name = ent["name"]
        is_variant = False
        for existing_name in list(seen.keys()):
            if name in existing_name or existing_name in name:
                if len(name) > len(existing_name):
                    del seen[existing_name]
                    seen[name] = ent
                is_variant = True
                break
        if not is_variant:
            seen[name] = ent
    return list(seen.values())


def resolve_entities(persons: List, orgs: List) -> Dict:
    normalized_persons = [
        {
            "name": normalize_person(p["name"]),
            "original": p["name"],
            "page": p.get("page"),
            "source": p.get("source", "unknown"),
            "sources": p.get("sources", []),
        }
        for p in persons if len(p.get("name", "")) > 2
    ]

    normalized_orgs = [
        {
            "name": normalize_org(o["name"]),
            "original": o["name"],
            "page": o.get("page"),
            "source": o.get("source", "unknown"),
            "sources": o.get("sources", []),
        }
        for o in orgs if len(o.get("name", "")) > 2
    ]

    return {
        "persons": deduplicate_entities(normalized_persons),
        "organizations": deduplicate_entities(normalized_orgs),
    }