from celery import Celery
REDIS_URL = "redis://redis:6379/0"

celery_app = Celery(
    "tasks",
    broker=REDIS_URL,
    backend=REDIS_URL,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    enable_utc=True,
    broker_connection_retry_on_startup=True,
)
celery_app.autodiscover_tasks(["launchpad.worker"], force=True)
