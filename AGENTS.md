# GenAI Launchpad — coding notes

Production foundation for event-driven GenAI applications. FastAPI + Celery + Redis + PostgreSQL (pgvector) + PydanticAI + Langfuse, orchestrated as DAG workflows of nodes that pass a shared `TaskContext`. Python 3.13.13, `uv`, Docker-based. See `README.md` to run it and [launchpad.datalumina.com](https://launchpad.datalumina.com/) for the full docs.

## Golden rules

- **Don't touch `app/launchpad/core/` unless the user specifically asks.** It's the Launchpad framework, treated as vendored. If you need different behavior, subclass the relevant `Node` / `Workflow` / `BaseRouter`.
- **Build with the existing patterns.** New workflows go in `app/launchpad/workflows/<your_workflow>/` with `schema.py`, `workflow.py`, `nodes/`, and (optional) `prompts/` and `request_examples/`. Register them in `app/launchpad/workflows/workflow_registry.py`. Mirror the layout of `app/launchpad/workflows/examples/quickstart/`.
- **Stay inside the existing structure.** Don't create new top-level folders, parallel `src/` trees, or stray scripts unless the user asks for one. New code lives under `app/launchpad/` (or `playground/` for local-only run scripts that match a registered workflow).
- **Reference workflows are demos.** The five examples under `app/launchpad/workflows/examples/` are reading material — copy from them, don't extend them with project-specific business logic.

## Workflows — the pattern

1. **Event schema** in `schema.py`: a Pydantic model describing the inbound event.
2. **Nodes** in `nodes/`: one node per file. Pick the right base:
   - `Node` — custom processing / data work.
   - `AgentNode` — LLM call via PydanticAI. Configure with `get_agent_config() -> AgentConfig`.
   - `ConcurrentNode` — run independent nodes in parallel.
   - `BaseRouter` / `RouterNode` — conditional branching using `get_output()` / `save_output()`.
3. **Workflow** in `workflow.py`: a `Workflow` subclass with a `workflow_schema = WorkflowSchema(...)` declaring `event_schema`, `start`, and `nodes` (list of `NodeConfig`).
4. **Register** the workflow class in `WorkflowRegistry` with a descriptive `UPPER_SNAKE_CASE` name — that name is the lookup key for the generic `/events` endpoint and Celery worker.
5. **Playground**: add `playground/<workflow>.py` to run it locally without API/Celery. Load a payload from `request_examples/`.

Compose workflows by calling a child workflow from a node and passing `context=` to `Workflow.run()` / `run_async()` — see `examples/nested_workflow/`.

## Prompts

Use Jinja2 templates via `launchpad.services.prompt_loader.PromptManager`. Two layouts — pick one per template:

- **Shared**: `app/launchpad/prompts/<name>.j2` — used by many workflows. `PromptManager.get_prompt("<name>", ...)`.
- **Colocated**: `app/launchpad/workflows/<workflow>/prompts/<name>.j2` — single-workflow. Pass `prompts_dir=Path(__file__).parent.parent / "prompts"`.

`StrictUndefined` is on. Use Jinja `default(...)` for optional vars. Put metadata in YAML frontmatter.

## LLM providers

Switch providers by changing `model_provider` in `AgentConfig`. Supported: OpenAI, Azure OpenAI, Anthropic, Google Gemini, Vertex AI, Bedrock, Ollama. Don't hardcode SDK clients in nodes — go through `AgentNode`.

## Dependencies — minimise

**Default: write it yourself. Reach for a library only when the alternative would be non-trivial, error-prone, or reinvention of a standard.**

Add deps with `uv add <pkg>`. Dev deps go in the `dev` group (`uv add --group dev <pkg>`). Same bar, just looser; prefer widely-used, low-footprint tools.

## Configuration

Environment lives in two `.env` files on purpose:
- `.env` at repo root — local Python dev (playground scripts, notebooks, `uv run …`).
- `docker/.env` — Docker Compose stack and Supabase services.

Don't sprinkle `os.getenv` / `load_dotenv` across modules. Centralise reads in a config module and import the resolved values.

## Code style

- Prefer stdlib: `pathlib`, `datetime`, `uuid`, `enum`, `dataclasses`, `asyncio`, `collections`, `itertools`, `json`, `urllib`.
- Small, obvious functions. A 15-line function with clear names beats a three-class abstraction.
- Don't add error handling, fallbacks, or validation for scenarios that can't happen. Trust internal callers and framework guarantees. Validate at boundaries (HTTP input, external APIs, DB).
- No premature abstraction: three similar lines is better than a badly-named base class. Extract when there's a third caller, not a hypothetical one.
- Type hints on public functions, node methods, and module-level things. Don't annotate every local.
- Async-only for network I/O in the request path and inside nodes. Celery tasks are sync entrypoints that may call async code via `asyncio.run`.
- Comments explain *why* when it's non-obvious, never *what*. Remove stale `# TODO`s.
- All data structures are Pydantic models — including `TaskContext` payloads and node `OutputType`s.

## Database

- PostgreSQL with `pgvector` for vectors. Access via `app/launchpad/database/session.py` and the repositories in `database/repository.py`.
- Every schema change goes through Alembic: `./app/launchpad/makemigration.sh "msg"` then `./app/launchpad/migrate.sh`. New ORM models must be imported where Alembic autogenerate can see them.

## Observability

- Langfuse for LLM tracing — enable per-workflow with `Workflow(enable_tracing=True)` and the `LANGFUSE_*` env vars. See `examples/langfuse_tracing/`.
- Log with stable, snake_case event names and keyword fields. No f-string log messages.

## Tests

- Prefer unit tests over integration. Mock at the service / node boundary.
- Don't test framework code under `core/`. Test workflow wiring, your nodes, and routers.
- Integration tests that need a running stack go behind a marker and stay out of the fast suite.