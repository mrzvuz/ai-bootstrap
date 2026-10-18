# Document search — retrieval-augmented generation

Two-node retrieval-and-generation workflow on top of the PostgreSQL + `pgvector` that already ships with the AI Bootstrap's Docker stack.

## What it demonstrates

- A plain `Node` (`RetrievalNode`) orchestrating a non-LLM side service (`PgvectorRAGService` in `services.py`) — no agent involved on the retrieval step.
- Retrieved documents passed to the generation node as typed dependencies.
- `vecs` for vector storage and OpenAI embeddings (`text-embedding-3-small`, 1536 dims) for query encoding — easy to swap.

## Workflow graph

```
RetrievalNode (Node) → embeds query, returns RetrievalResults
        ↓
GenerationNode (AgentNode) → uses retrieved context to answer, returns
                             {answer, sources, confidence}
```

## Event schema

```python
class RagExampleEventSchema(BaseModel):
    query: str
```

## Run it

1. Bring the Docker stack up so Postgres + pgvector are available (`cd docker && ./start.sh`), and apply migrations from `app/ai_bootstrap/` (`./migrate.sh`).

2. Seed the collection with something to retrieve:

   ```python
   import vecs
   from openai import OpenAI

   from ai_bootstrap.database.database_utils import DatabaseUtils

   client = vecs.create_client(DatabaseUtils.get_connection_string())
   collection = client.get_or_create_collection(name="docs", dimension=1536)
   embedding = OpenAI().embeddings.create(
       input=["Vector search enables semantic retrieval."],
       model="text-embedding-3-small",
   ).data[0].embedding
   collection.upsert(records=[("doc-1", embedding, {"source": "handbook"})])
   client.disconnect()
   ```

3. Run the workflow:

   ```bash
   uv run playground/rag.py
   ```

   Loads [`request_examples/query.json`](./request_examples/) and prints the answer with sources and confidence.

Registered as `WorkflowRegistry.RAG`.

## Customize

- Swap the embedding model by passing a different `embedding_model` to `PgvectorRAGService` (or replace it with a non-OpenAI embedding client altogether).
- Adjust retrieval: change `limit`, `measure`, or add metadata filters in `RetrievalNode.process()`.
- Chain additional nodes between `RetrievalNode` and `GenerationNode` (reranking, source filtering, etc.) — they just read the retrieval output via `self.get_output(RetrievalNode)`.
