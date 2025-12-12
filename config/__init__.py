from .celery import app as celery_app

__all__ = ('celery_app')

#this made django understand that celery is part of the project