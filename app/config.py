import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    NEO4J_URI: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER: str = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD", "password")
    SPACY_MODEL: str = "en_core_web_sm"

settings = Settings()
