from ai_bootstrap.core.schema import WorkflowSchema, NodeConfig
from ai_bootstrap.core.workflow import Workflow
from ai_bootstrap.workflows.examples.customer_support.schema import CustomerCareEventSchema
from ai_bootstrap.workflows.examples.customer_support.nodes.analyze_ticket_node import AnalyzeTicketNode
from ai_bootstrap.workflows.examples.customer_support.nodes.close_ticket_node import CloseTicketNode
from ai_bootstrap.workflows.examples.customer_support.nodes.determine_intent_ticket_node import (
    DetermineTicketIntentNode,
)
from ai_bootstrap.workflows.examples.customer_support.nodes.escalate_ticket_node import EscalateTicketNode
from ai_bootstrap.workflows.examples.customer_support.nodes.filter_spam import FilterSpamNode
from ai_bootstrap.workflows.examples.customer_support.nodes.generate_response_node import GenerateResponseNode
from ai_bootstrap.workflows.examples.customer_support.nodes.process_invoice_node import ProcessInvoiceNode
from ai_bootstrap.workflows.examples.customer_support.nodes.send_reply_node import SendReplyNode
from ai_bootstrap.workflows.examples.customer_support.nodes.ticket_router_node import TicketRouterNode
from ai_bootstrap.workflows.examples.customer_support.nodes.validate_ticket_node import ValidateTicketNode


class CustomerCareWorkflow(Workflow):
    workflow_schema = WorkflowSchema(
        description="",
        event_schema=CustomerCareEventSchema,
        start=AnalyzeTicketNode,
        nodes=[
            NodeConfig(
                node=AnalyzeTicketNode,
                connections=[TicketRouterNode],
                description="",
                concurrent_nodes=[
                    DetermineTicketIntentNode,
                    FilterSpamNode,
                    ValidateTicketNode,
                ],
            ),
            NodeConfig(
                node=TicketRouterNode,
                connections=[
                    CloseTicketNode,
                    EscalateTicketNode,
                    GenerateResponseNode,
                    ProcessInvoiceNode,
                ],
                description="",
                is_router=True,
            ),
            NodeConfig(
                node=GenerateResponseNode,
                connections=[SendReplyNode],
                description="",
            ),
        ],
    )
