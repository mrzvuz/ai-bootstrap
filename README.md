# AI Bootstrap

AI Bootstrap is a Python starter project for event driven AI applications. It combines FastAPI, Celery, Redis, PostgreSQL with pgvector, PydanticAI, and Langfuse.

Workflows are built as graphs of small nodes. Each node reads and updates a shared `TaskContext`; the API accepts events and Celery runs their workflows in the background.

## Repository layout

```text
app/ai_bootstrap/
  api/             FastAPI endpoints
  core/            Workflow, node, and routing primitives
  database/        SQLAlchemy models and database access
  services/        Shared application services
  workflows/       Workflow registry and runnable examples
  worker/          Celery application and event tasks
  start.sh         Run migrations and start the API
docker/            Docker Compose, Dockerfiles, and service configuration
playground/         Local runners for the example workflows
```

## Requirements

- Python 3.13.13
- [`uv`](https://docs.astral.sh/uv/)
- Docker and Docker Compose for the full service stack
- An OpenAI API key for the LLM examples

## Local setup

Create the local environment files and install the project:

```bash
cp .env.example .env
cp docker/.env.example docker/.env
uv sync
```

Set the required API keys in `.env`. Run a workflow directly with a playground script, for example:

```bash
uv run playground/customer_support.py
```

## Run the service stack

Configure `docker/.env`, then start the API, worker, Redis, and PostgreSQL:

```bash
cd docker
./start.sh
```

Apply database migrations from the package directory:

```bash
cd app/ai_bootstrap
./migrate.sh
```

The API listens on `http://localhost:8080`. `POST /events/` stores and queues a workflow event. `POST /v1/chat/completions` streams a chat response using Server-Sent Events.

## Example workflows

| Example | Purpose | Runner |
| --- | --- | --- |
| Customer support | Parallel ticket analysis and routing | `uv run playground/customer_support.py` |
| Nested workflow | A parent workflow calls a reply drafting workflow | `uv run playground/nested_workflow.py` |
| Streaming | Text and structured chat output over SSE | `uv run playground/streaming.py` |
| Moderation | Comment review with Langfuse tracing | `uv run playground/moderation.py` |
| Retrieval augmented generation | Search pgvector and answer from retrieved documents | `uv run playground/rag.py` |

See [`app/ai_bootstrap/workflows/examples/`](app/ai_bootstrap/workflows/examples/README.md) for details and sample payloads.

## Build a workflow

Create a workflow directory under `app/ai_bootstrap/workflows/` with an event schema, node modules, and a workflow class. Add the workflow to [`WorkflowRegistry`](app/ai_bootstrap/workflows/workflow_registry.py) so the event API and worker can select it. Use the examples as working references.

## Configuration

- `.env` configures local Python runs.
- `docker/.env` configures Docker Compose services.
- Database settings use `DATABASE_HOST`, `DATABASE_NAME`, `DATABASE_USER`, `DATABASE_PASSWORD`, and `DATABASE_PORT`.
- LLM provider and Langfuse settings are read by their existing provider integrations.

## Database migrations

From `app/ai_bootstrap/`, create a migration and apply it:

```bash
./makemigration.sh "describe the schema change"
./migrate.sh
```
