from pydantic import BaseModel
import vecs
from openai import OpenAI

from launchpad.database.database_utils import DatabaseUtils


class Record(BaseModel):
    id: str
    metadata: dict


class RetrievalResults(BaseModel):
    results: list[Record]


class PgvectorRAGService:
    def __init__(self, collection_name: str = "docs", embedding_model: str = "text-embedding-3-small"):
        self.vector_client = vecs.create_client(DatabaseUtils.get_connection_string())
        self.collection = self.vector_client.get_or_create_collection(
            name=collection_name, dimension=1536
        )
        self.client = OpenAI()
        self.embedding_model = embedding_model

    def get_embedding(self, text: str) -> list[float]:
        text = text.replace("\n", " ")
        return (
            self.client.embeddings.create(input=[text], model=self.embedding_model)
            .data[0]
            .embedding
        )

    def parse_results(
        self, results: list[tuple[str, list[float], dict]]
    ) -> RetrievalResults:
        return RetrievalResults(
            results=[Record(id=record_id, metadata=metadata) for record_id, _, metadata in results]
        )

    def disconnect(self):
        self.vector_client.disconnect()
