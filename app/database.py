from neo4j import GraphDatabase
from .config import settings

class Neo4jConnection:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
        )

    def close(self):
        self.driver.close()

    def create_memory(self, memory_data):
        with self.driver.session() as session:
            result = session.write_transaction(self._create_and_return_memory, memory_data)
            return result

    @staticmethod
    def _create_and_return_memory(tx, memory_data):
        query = """
        MERGE (u:User {id: $user_id})
        CREATE (m:Memory {id: apoc.create.uuid(), title: $title, date: $date, context: $context})
        MERGE (u)-[:CREATED]->(m)
        WITH m
        UNWIND $media AS mediaItem
        CREATE (media:Media {url: mediaItem.url, type: mediaItem.type})
        MERGE (m)-[:CONTAINS]->(media)
        WITH m
        UNWIND $people AS personName
        MERGE (p:Person {name: personName})
        MERGE (m)-[:INVOLVES]->(p)
        WITH m
        MERGE (loc:Location {name: $location})
        MERGE (m)-[:TAKES_PLACE_AT]->(loc)
        WITH m
        MERGE (e:Event {name: $event})
        MERGE (m)-[:IS_A]->(e)
        RETURN m
        """
        result = tx.run(query, **memory_data)
        return result.single()

    def search_memories_basic(self, title=None, date=None):
        with self.driver.session() as session:
            result = session.read_transaction(self._search_basic, title, date)
            return result

    @staticmethod
    def _search_basic(tx, title, date):
        query = """
        MATCH (m:Memory)
        WHERE ($title IS NULL OR m.title CONTAINS $title)
          AND ($date IS NULL OR m.date = $date)
        RETURN m LIMIT 50
        """
        result = tx.run(query, title=title, date=date)
        return [record["m"] for record in result]

    def search_memories_advanced(self, cypher_query):
        with self.driver.session() as session:
            result = session.read_transaction(self._run_cypher, cypher_query)
            return result

    @staticmethod
    def _run_cypher(tx, cypher_query):
        result = tx.run(cypher_query)
        return [record["m"] for record in result]


neo4j_conn = Neo4jConnection()
