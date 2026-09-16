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
Playground for the quickstart (customer care) example workflow.

Swap the request_example file below for any of:
  invoice.json, policy_question.json, product.json, prompt_injection.json,
  refund.json, service_desk.json, spam.json
"""

event_path = (
    project_root
    / "app/launchpad/workflows/examples/quickstart/request_examples/invoice.json"
)
with open(event_path) as f:
    event = json.load(f)

workflow = WorkflowRegistry.QUICKSTART.value()
output = workflow.run(event)

print(output.model_dump_json(indent=2))
