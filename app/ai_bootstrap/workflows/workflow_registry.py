from enum import Enum

from ai_bootstrap.workflows.examples.streaming.workflow import ExampleStreamingWorkflow
from ai_bootstrap.workflows.examples.customer_support.workflow import CustomerCareWorkflow
from ai_bootstrap.workflows.examples.moderation.workflow import (
    LangfuseTracingWorkflow,
)
from ai_bootstrap.workflows.examples.nested_workflow.workflow import (
    NestedWorkflow,
)
from ai_bootstrap.workflows.examples.rag.workflow import RagExampleWorkflow


class WorkflowRegistry(Enum):
    STREAMING = ExampleStreamingWorkflow
    CUSTOMER_SUPPORT = CustomerCareWorkflow
    MODERATION = LangfuseTracingWorkflow
    RAG = RagExampleWorkflow
    NESTED_WORKFLOW = NestedWorkflow
