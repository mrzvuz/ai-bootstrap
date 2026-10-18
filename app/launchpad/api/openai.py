from fastapi import APIRouter
from starlette.responses import StreamingResponse

from launchpad.workflows.examples.streaming.schema import OpenAIChatSchema
from launchpad.utils.event_stream_generator import event_stream_generator
from launchpad.workflows.examples.streaming.workflow import ExampleStreamingWorkflow

router = APIRouter()


@router.post("/chat/completions")
async def handle_chat_completion_streaming(data: OpenAIChatSchema) -> StreamingResponse:
    workflow = ExampleStreamingWorkflow(enable_tracing=True)
    return StreamingResponse(
        event_stream_generator(workflow.run_stream_async(data.model_dump())),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
