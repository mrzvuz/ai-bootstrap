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
Playground for the customer support example workflow.

Swap the request_example file below for any of:
  invoice.json, policy_question.json, product.json, prompt_injection.json,
  refund.json, service_desk.json, spam.json
"""

event_path = (
    project_root
    / "app/ai_bootstrap/workflows/examples/customer_support/request_examples/invoice.json"
)
with open(event_path) as f:
    event = json.load(f)

workflow = WorkflowRegistry.CUSTOMER_SUPPORT.value()
output = workflow.run(event)

print(output.model_dump_json(indent=2))
