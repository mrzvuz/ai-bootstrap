# Example workflows

These runnable examples show the main workflow patterns in AI Bootstrap. Copy an example into `app/ai_bootstrap/workflows/` when starting a project workflow.

Each example keeps its schema, workflow, nodes, sample requests, and optional prompts together. The application registers them in [`workflow_registry.py`](../workflow_registry.py).

| Example | Demonstrates | Playground |
| --- | --- | --- |
| [`customer_support/`](./customer_support/) | Parallel ticket analysis, routing, and prompt templates | `uv run playground/customer_support.py` |
| [`nested_workflow/`](./nested_workflow/) | Minimal nested workflow composition with a parent node calling a child workflow | `uv run playground/nested_workflow.py` |
| [`streaming/`](./streaming/) | SSE streaming through `run_stream_async`, text + structured output | `uv run playground/streaming.py` |
| [`moderation/`](./moderation/) | Comment moderation with Langfuse tracing | `uv run playground/moderation.py` |
| [`rag/`](./rag/) | Retrieval-augmented generation against `pgvector` | `uv run playground/rag.py` |

To remove an example, delete its directory and remove its entry from `WorkflowRegistry`.
