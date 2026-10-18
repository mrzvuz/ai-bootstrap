# AI Bootstrap — repository instructions

This repository is a Python 3.13.13 application starter for event driven AI workflows. It uses FastAPI, Celery, Redis, PostgreSQL with pgvector, PydanticAI, and Langfuse. Use `README.md` for setup and runtime commands.

## Project structure

- Application package: `app/ai_bootstrap/`.
- Workflow code and examples: `app/ai_bootstrap/workflows/`.
- Local workflow runners: `playground/`.
- Docker Compose and service configuration: `docker/`.

Keep changes inside this structure. Follow the closest existing example when adding a workflow.

## Workflow pattern

1. Define the inbound event as a Pydantic model in `schema.py`.
2. Implement one node per file under `nodes/`. Use `Node` for processing, `AgentNode` for model calls, `ConcurrentNode` for independent work, and router nodes for conditional paths.
3. Define the workflow graph in `workflow.py` with `WorkflowSchema` and `NodeConfig`.
4. Add the workflow class to `workflows/workflow_registry.py`.
5. Add a playground runner and sample event when the workflow should be runnable locally.

Use Jinja templates with `PromptManager` for prompts. Keep prompts in the workflow's `prompts/` directory when used by one workflow, or in `app/ai_bootstrap/prompts/` when shared.

## Implementation style

- Prefer direct, readable control flow and descriptive names.
- Use the standard library unless a dependency removes meaningful complexity.
- Validate input at external boundaries; rely on internal type and framework guarantees.
- Add type hints to public functions and node methods.
- Use async I/O in request handlers and workflow nodes. Celery task entrypoints remain synchronous.
- Keep comments for non-obvious reasoning, not narration.
- Store structured application data in Pydantic models.

## Configuration and data

- `.env` is for local Python runs; `docker/.env` is for the container stack.
- Read database settings through `database/database_utils.py`.
- Apply schema changes with the Alembic scripts in `app/ai_bootstrap/`.
- Keep ORM models importable from Alembic's environment module.

## Logging and tracing

Use stable snake_case log event names and keyword fields. Enable Langfuse tracing per workflow when required by the use case.

## Tests

Prefer focused unit tests around application boundaries. Integration checks that require Docker services should be kept separate from the fast test suite.
