import spacy
from config import SPACY_MODEL


def add_entity_ruler(nlp):
    ruler = nlp.add_pipe("entity_ruler", before="ner")
    patterns = [
        {"label": "ORG", "pattern": [{"IS_TITLE": True}, {"ORTH": "Holding"}]},
        {"label": "ORG", "pattern": [{"IS_TITLE": True}, {"ORTH": "SARL"}]},
        {"label": "ORG", "pattern": [{"IS_TITLE": True}, {"ORTH": "SA"}]},
        {
            "label": "PER",
            "pattern": [
                {"LOWER": {"IN": ["monsieur", "m.", "mme", "madame"]}},
                {"IS_TITLE": True},
                {"IS_TITLE": True, "OP": "?"},
            ],
        },
    ]
    ruler.add_patterns(patterns)
    return nlp


def load_model_with_rules():
    nlp = spacy.load(SPACY_MODEL)
    return add_entity_ruler(nlp)