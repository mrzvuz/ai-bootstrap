from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from ai_bootstrap.database.event import Event
from ai_bootstrap.database.repository import GenericRepository
from ai_bootstrap.database.session import db_session
from ai_bootstrap.worker.config import celery_app
from ai_bootstrap.workflows.workflow_registry import WorkflowRegistry

router = APIRouter()


@router.post("/")
def handle_event(
    data: dict,
    session: Session = Depends(db_session),
) -> Response:
    """Store an event and queue it for workflow processing."""
    repository = GenericRepository(
        session=session,
        model=Event,
    )
    event = Event(data=data, workflow_type=get_workflow_type())
    repository.create(obj=event)

    task_id = celery_app.send_task(
        "process_incoming_event",
        args=[str(event.id)],
    )

    return JSONResponse(
        content={"message": f"process_incoming_event started `{task_id}`"},
        status_code=HTTPStatus.ACCEPTED,
    )


def get_workflow_type() -> str:
    return WorkflowRegistry.CUSTOMER_SUPPORT.name
