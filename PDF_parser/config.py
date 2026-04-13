import os

BASE_DIR = os.path.dirname(__file__)
INPUT_DIR = os.path.join(BASE_DIR, "data", "input")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "output")
MIN_TEXT_LENGTH = 50
MAX_PAGES = 100
OCR_FALLBACK = False

DOC_TYPES = {
    "kyc": ["beneficiaire", "identite", "passeport", "cin"],
    "statuts": ["statut", "constitution", "capital social"],
    "rc": ["registre", "commerce", "immatriculation"],
    "pv": ["proces-verbal", "assemblee", "resolution"],
}
