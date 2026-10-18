from launchpad.database.event import Event
from launchpad.database.repository import GenericRepository
from launchpad.database.session import db_session
from launchpad.worker.config import celery_app
from launchpad.workflows.workflow_registry import WorkflowRegistry

@celery_app.task(name="process_incoming_event")
def process_incoming_event(event_id: str):
    """Run the workflow attached to a stored event."""
    session_generator = db_session()
    session = next(session_generator)
    try:
        repository = GenericRepository(session=session, model=Event)
        event = repository.get(id=event_id)
        if event is None:
            raise ValueError(f"Event with id {event_id} not found")

        workflow = WorkflowRegistry[event.workflow_type].value()
        event.task_context = workflow.run(event.data).model_dump(mode="json")
        repository.update(obj=event)
    finally:
        session_generator.close()
