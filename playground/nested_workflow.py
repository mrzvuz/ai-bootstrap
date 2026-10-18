import json
import logging
from pathlib import Path

import nest_asyncio
from dotenv import load_dotenv

project_root = Path(__file__).parent.parent

load_dotenv(project_root / ".env")

from ai_bootstrap.workflows.workflow_registry import WorkflowRegistry  # noqa: E402

logging.basicConfig(level=logging.INFO)
nest_asyncio.apply()

event_path = (
    project_root
    / "app/ai_bootstrap/workflows/examples/nested_workflow/request_examples/billing_question.json"
)
with open(event_path) as f:
    event = json.load(f)

workflow = WorkflowRegistry.NESTED_WORKFLOW.value()
output = workflow.run(event)

print(output.model_dump_json(indent=2))
