import os
from dotenv import load_dotenv

load_dotenv()

SPACY_MODEL = "fr_core_news_md"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-1.5-flash"

PERSON_LABELS = ["PER", "PERSON"]
ORG_LABELS = ["ORG"]

LEGAL_SUFFIXES = [
    "SARL", "SA", "SAS", "SASU", "SCI",
    "Holding", "Group", "Ltd", "GmbH",
    "Bank", "Banque", "Capital", "Finance"
]

ROLES = [
    "gerant", "directeur", "president", "actionnaire",
    "associe", "representant", "mandataire", "PDG", "DG"
]

HIGH_CONF = "high"
MEDIUM_CONF = "medium"
LOW_CONF = "low"