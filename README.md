# AI Bootstrap

AI Bootstrap is a Docker-based starter kit for building production-ready GenAI applications.

It includes FastAPI, Celery, PostgreSQL with vector support, Redis, optional Caddy and Supabase services, workflow orchestration, background processing, streaming, tracing, and example AI workflows.

## Overview

AI Bootstrap gives you the core infrastructure and workflow patterns needed to build GenAI applications on one branch: `main`.

Use the application code as the foundation, study the examples in `workflows`, and run them locally from `playground`.

## Project Structure

```text
app/
  launchpad/
    alembic/            Database migrations
    api/                FastAPI routes
    core/               Workflow, node, routing, and validation primitives
    database/           Database models, sessions, and repositories
    prompts/            Shared prompt templates
    schemas/            Shared schemas
    services/           Shared application services
    utils/              Utility functions
    worker/             Celery worker configuration and tasks
    workflows/          Workflow definitions, registry, and examples
    main.py             FastAPI application entrypoint
    migrate.sh          Run database migrations
    makemigration.sh    Create database migrations

docker/                 Docker, Caddy, Supabase, and service configuration
playground/             Scripts for running workflows locally
pyproject.toml          Python project configuration
```

## Installation

Install Python 3.13.13 and `uv`, copy the example environment files, then install dependencies:

```bash
cp .env.example .env
cp docker/.env.example docker/.env
uv sync
```

Start the Docker services from `docker/` with `./start.sh`, then apply database migrations from `app/launchpad/` with `./migrate.sh`.

There are two environment files on purpose:

- `.env` at the repo root is for local development with your local Python environment, including playground scripts, unit tests, notebooks, and one-off `uv run ...` commands.
- `docker/.env` is for Docker Compose, the fully containerized application stack, the database, and optional Supabase services. It is much larger mostly because self-hosted Supabase requires many settings even though Supabase is excluded by default.

## Workflows

Example workflows live in `app/launchpad/workflows/examples/`.

They show how to build workflows with nodes, routers, schemas, prompts, tracing, streaming, and retrieval.

Current examples:

- `quickstart`: customer-care workflow with concurrent analysis, routing, and Jinja2 prompts.
- `nested_workflow`: minimal customer-care workflow that delegates reply drafting to a child workflow.
- `streaming`: server-sent event streaming with text and structured outputs.
- `langfuse_tracing`: multi-node moderation workflow with Langfuse tracing.
- `pgvector_rag`: retrieval-augmented generation using PostgreSQL and pgvector.

## Playground

After installation, use the playground scripts to run examples locally without going through the API.

```bash
uv run playground/quickstart.py
uv run playground/nested_workflow.py
uv run playground/streaming.py
uv run playground/langfuse_tracing.py
uv run playground/pgvector_rag.py
```

Each script loads an example request from the matching workflow directory.

## Documentation

Setup and workflow documentation is maintained in this repository and in each example workflow's README.
