from ai_bootstrap.core.schema import WorkflowSchema, NodeConfig
from ai_bootstrap.core.workflow import Workflow
from ai_bootstrap.workflows.examples.streaming.schema import OpenAIChatSchema
from ai_bootstrap.workflows.examples.streaming.nodes.text_streaming_node import TextStreamingNode
from ai_bootstrap.workflows.examples.streaming.nodes.structured_streaming_node import (
    StructuredStreamingNode,
)


class ExampleStreamingWorkflow(Workflow):
    workflow_schema = WorkflowSchema(
        description="",
        event_schema=OpenAIChatSchema,
        start=TextStreamingNode,
        nodes=[
            NodeConfig(
                node=TextStreamingNode,
                connections=[StructuredStreamingNode],
                description="",
            ),
            NodeConfig(
                node=StructuredStreamingNode,
                connections=[],
                description="",
            ),
        ],
    )
