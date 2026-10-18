from ai_bootstrap.core.schema import WorkflowSchema, NodeConfig
from ai_bootstrap.core.workflow import Workflow
from ai_bootstrap.workflows.examples.moderation.schema import LangfuseTracingEventSchema
from ai_bootstrap.workflows.examples.moderation.nodes.context_summary_result_node import (
    ContextSummaryResult,
)
from ai_bootstrap.workflows.examples.moderation.nodes.remove_comment_node import RemoveCommentNode
from ai_bootstrap.workflows.examples.moderation.nodes.violation_detection_node import (
    ViolationDetectionNode,
)


class LangfuseTracingWorkflow(Workflow):
    workflow_schema = WorkflowSchema(
        description="",
        event_schema=LangfuseTracingEventSchema,
        start=ViolationDetectionNode,
        nodes=[
            NodeConfig(
                node=ViolationDetectionNode,
                connections=[ContextSummaryResult],
                description="",
            ),
            NodeConfig(
                node=ContextSummaryResult,
                connections=[RemoveCommentNode],
                description="",
            ),
            NodeConfig(
                node=RemoveCommentNode,
                connections=[],
                description="",
            ),
        ],
    )
