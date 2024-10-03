import spacy
from typing import Dict, List

class MetadataExtractor:
    def __init__(self, model_name: str):
        self.nlp = spacy.load(model_name)

    def extract(self, text: str) -> Dict:
        doc = self.nlp(text)
        entities = {ent.label_: ent.text for ent in doc.ents}

        # Example: Extract date, person, location, etc.
        metadata = {
            "date": entities.get("DATE"),
            "people": self._extract_entities(doc, "PERSON"),
            "location": entities.get("GPE") or entities.get("LOC"),
            "event": entities.get("EVENT") or entities.get("ORG"),
        }

        return metadata

    def _extract_entities(self, doc, label: str) -> List[str]:
        return [ent.text for ent in doc.ents if ent.label_ == label]
