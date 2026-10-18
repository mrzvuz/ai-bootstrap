from ai_bootstrap.core.schema import NodeConfig, WorkflowSchema
from ai_bootstrap.core.workflow import Workflow
from ai_bootstrap.workflows.examples.nested_workflow.nodes.run_reply_workflow_node import (
    RunReplyWorkflowNode,
)
from ai_bootstrap.workflows.examples.nested_workflow.nodes.send_reply_node import (
    SendReplyNode,
)
from ai_bootstrap.workflows.examples.nested_workflow.schema import (
    NestedWorkflowEventSchema,
)


class NestedWorkflow(Workflow):
    workflow_schema = WorkflowSchema(
        description="Parent workflow that delegates reply drafting to a child workflow.",
        event_schema=NestedWorkflowEventSchema,
        start=RunReplyWorkflowNode,
        nodes=[
            NodeConfig(
                node=RunReplyWorkflowNode,
                connections=[SendReplyNode],
                description="Calls ReplyDraftWorkflow with the shared context.",
            ),
        ],
    )
