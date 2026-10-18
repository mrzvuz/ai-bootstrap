from ai_bootstrap.core.schema import WorkflowSchema, NodeConfig
from ai_bootstrap.core.workflow import Workflow
from ai_bootstrap.workflows.examples.rag.schema import RagExampleEventSchema
from ai_bootstrap.workflows.examples.rag.nodes.retrieval_node import RetrievalNode
from ai_bootstrap.workflows.examples.rag.nodes.generation_node import GenerationNode


class RagExampleWorkflow(Workflow):
    workflow_schema = WorkflowSchema(
        description="Simple RAG example workflow",
        event_schema=RagExampleEventSchema,
        start=RetrievalNode,
        nodes=[
            NodeConfig(
                node=RetrievalNode,
                connections=[GenerationNode],
                description="",
            ),
            NodeConfig(
                node=GenerationNode,
                connections=[],
                description="",
            ),
        ],
    )
