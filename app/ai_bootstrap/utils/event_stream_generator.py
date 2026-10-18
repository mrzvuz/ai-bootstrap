import json
import logging
from typing import AsyncIterator


async def event_stream_generator(workflow_stream: AsyncIterator) -> AsyncIterator[str]:
    try:
        async for event in workflow_stream:
            yield f"data: {json.dumps(event)}\n\n"
        yield "data: [DONE]\n\n"
    except Exception as e:
        logging.exception("event_stream_failed")
        error_event = {"type": "error", "error": str(e)}
        yield f"data: {json.dumps(error_event)}\n\n"
        raise
