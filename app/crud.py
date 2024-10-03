import spacy

nlp = spacy.load("en_core_web_sm")

def extract_metadata(text: str):
    doc = nlp(text)
    metadata = {
        "entities": [],
        "dates": [],
        "locations": [],
        "keywords": []
    }

    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC"]:
            metadata["locations"].append(ent.text)
        elif ent.label_ == "DATE":
            metadata["dates"].append(ent.text)
        elif ent.label_ in ["PERSON", "ORG", "PRODUCT"]:
            metadata["entities"].append(ent.text)

    metadata["keywords"] = list(set(metadata["locations"] + metadata["entities"]))
    return metadata
