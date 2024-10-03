from fastapi import FastAPI, HTTPException
from neo4j import GraphDatabase

from .config import settings
from .database import MemoryGraph
from .models import CreateMemoryRequest, MemoryResponse, NaturalLanguageSearchRequest, NaturalLanguageSearchResponse, \
    Memory
from .crud import  extract_metadata
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Memory Sharing Platform")

# Enable CORS if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
driver = GraphDatabase.driver(
    settings.NEO4J_URI,
    auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
)

@app.post("/memories/")
async def create_memory(memory: Memory):
    metadata = extract_metadata(memory.text)

    with driver.session() as session:
        # Create a memory node and related nodes for entities, dates, and locations
        try:
            query = """
            CREATE (m:Memory {text: $text})
            WITH m
            FOREACH (location IN $locations |
                MERGE (loc:Location {name: location})
                MERGE (m)-[:LOCATED_AT]->(loc))
            WITH m
            FOREACH (date IN $dates |
                MERGE (d:Date {date: date})
                MERGE (m)-[:OCCURRED_ON]->(d))
            WITH m
            FOREACH (entity IN $entities |
                MERGE (e:Entity {name: entity})
                MERGE (m)-[:RELATED_TO]->(e))
            RETURN m
            """
            session.run(query, {
                "text": memory.text,
                "locations": metadata["locations"],
                "dates": metadata["dates"],
                "entities": metadata["entities"]
            })
            return {"message": "Memory created successfully!"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@app.post("/memories/search/", response_model=NaturalLanguageSearchResponse)
def api_search_memories_natural(natural_request: NaturalLanguageSearchRequest):
    print('updated script')
    with driver.session() as session:
        try:
            search_query = """
               MATCH (m:Memory)-[:LOCATED_AT|OCCURRED_ON|RELATED_TO]->(n)
               WHERE m.text CONTAINS $query
               RETURN m, collect(n) as relatedNodes
               """
            result = session.run(search_query, {"query": natural_request})
            memories = []
            for record in result:
                memories.append({
                    "memory": record["m"]["text"],
                    "related_nodes": [node["name"] for node in record["relatedNodes"]]
                })
            return {"results": memories}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
