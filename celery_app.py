from celery import Celery
import os

REDIS_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")

celery_app = Celery(
    main='celery_worker', 
    broker=REDIS_URL, 
    backend=REDIS_URL,
    include=['tasks']
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="America/New_York",
    enable_utc=True,
    result_expires=3600,  #results expire in Redis after 1 hour
)