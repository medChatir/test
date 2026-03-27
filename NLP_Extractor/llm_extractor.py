import json
import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(GEMINI_MODEL)

SYSTEM_PROMPT = """
Tu es un assistant spécialisé en analyse de documents juridiques et KYC.
Tu dois extraire les entités et relations sous format JSON strict.
"""


def extract_with_llm(chunk_text: str, spacy_persons: list, spacy_orgs: list) -> dict:
    prompt = f"""
{SYSTEM_PROMPT}

Texte :
{chunk_text[:2000]}

Entités détectées par spaCy :
Personnes : {', '.join(spacy_persons) or 'Aucune'}
Organisations : {', '.join(spacy_orgs) or 'Aucune'}

Retourne uniquement du JSON valide, sans texte autour, sans backticks.
Format attendu :
{{
  "persons": [{{"name": ""}}],
  "organizations": [{{"name": ""}}],
  "relations": [
    {{"source": "", "target": "", "type": "", "percentage": ""}}
  ]
}}
"""
    try:
        response = model.generate_content(
            prompt,
            generation_config={"temperature": 0}
        )
        text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"Gemini error: {e}")
        return {"persons": [], "organizations": [], "relations": []}