from ai_bootstrap.core.schema import NodeConfig, WorkflowSchema
from ai_bootstrap.core.workflow import Workflow
from ai_bootstrap.workflows.examples.nested_workflow.nodes.reply.draft_reply_node import (
    DraftReplyNode,
)
from ai_bootstrap.workflows.examples.nested_workflow.schema import (
    NestedWorkflowEventSchema,
)


class ReplyDraftWorkflow(Workflow):
    workflow_schema = WorkflowSchema(
        description="Child workflow that drafts a customer-care reply.",
        event_schema=NestedWorkflowEventSchema,
        start=DraftReplyNode,
        nodes=[
            NodeConfig(
                node=DraftReplyNode,
                description="Drafts a deterministic reply for the customer.",
            ),
        ],
    )
