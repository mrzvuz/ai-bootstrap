import json
import logging
from pathlib import Path

import nest_asyncio
from dotenv import load_dotenv

project_root = Path(__file__).parent.parent

load_dotenv(project_root / ".env")

from launchpad.workflows.workflow_registry import WorkflowRegistry

logging.basicConfig(level=logging.INFO)
nest_asyncio.apply()

"""
Playground for the pgvector_rag example workflow.

Prerequisite: a `docs` collection in pgvector with embedded documents to
retrieve. Without documents, the retrieval step returns empty results.
"""

event_path = (
    project_root / "app/launchpad/workflows/examples/pgvector_rag/request_examples/query.json"
)
with open(event_path) as f:
    event = json.load(f)

workflow = WorkflowRegistry.PGVECTOR_RAG.value()
output = workflow.run(event)

print(output.model_dump_json(indent=2))
