HIGH_CONF = "high"
MEDIUM_CONF = "medium"
LOW_CONF = "low"


def compute_confidence(entity: dict) -> str:
    sources = set(entity.get("sources", []))
    if "spacy" in sources and "llm" in sources:
        return HIGH_CONF
    elif "spacy" in sources and "rule" in sources:
        return HIGH_CONF
    elif "spacy" in sources:
        return MEDIUM_CONF
    elif "rule" in sources:
        return MEDIUM_CONF
    else:
        return LOW_CONF


def score_all_entities(entities: list) -> list:
    for entity in entities:
        entity["confidence"] = compute_confidence(entity)
    return entities