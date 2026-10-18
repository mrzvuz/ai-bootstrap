import asyncio
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
Playground for the streaming example workflow.

Streams chunks from each node in order. Uses run_stream_async so we need an
asyncio event loop.
"""


async def main() -> None:
    event_path = (
        project_root / "app/ai_bootstrap/workflows/examples/streaming/request_examples/chat.json"
    )
    with open(event_path) as f:
        event = json.load(f)

    workflow = WorkflowRegistry.STREAMING.value()
    async for chunk in workflow.run_stream_async(event):
        print(chunk)


asyncio.run(main())
