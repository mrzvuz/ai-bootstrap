import json
import logging
from pathlib import Path

import nest_asyncio
from dotenv import load_dotenv

project_root = Path(__file__).parent.parent

load_dotenv(project_root / ".env")

from ai_bootstrap.workflows.workflow_registry import WorkflowRegistry

logging.basicConfig(level=logging.INFO)
nest_asyncio.apply()

"""
Playground for the RAG example workflow.

Prerequisite: a `docs` collection in pgvector with embedded documents to
retrieve. Without documents, the retrieval step returns empty results.
"""

event_path = (
    project_root / "app/ai_bootstrap/workflows/examples/rag/request_examples/query.json"
)
with open(event_path) as f:
    event = json.load(f)

workflow = WorkflowRegistry.RAG.value()
output = workflow.run(event)

print(output.model_dump_json(indent=2))
