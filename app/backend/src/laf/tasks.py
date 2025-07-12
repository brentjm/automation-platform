import os
import time
import random
import requests
from celery import Celery

celery = Celery(__name__)
celery.config_from_object('laf.config:Config', namespace='CELERY')

BACKEND_URL = os.environ.get("BACKEND_URL", "http://web:5000")

@celery.task(bind=True)
def run_instrument_task(self, task_id, instrument_name):
    """
    A Celery task to trigger a mock instrument.
    """
    instrument_url = f"http://{instrument_name}:5001"
    try:
        # Update task status to 'running' via webhook
        requests.post(f"{BACKEND_URL}/api/webhook/task/update", json={'task_id': task_id, 'status': 'running'})

        # Call the instrument to start its process
        response = requests.post(f"{instrument_url}/run", json={'task_id': task_id})
        response.raise_for_status()
        return {"status": "instrument process started", "instrument_response": response.json()}
    except requests.exceptions.RequestException as e:
        # Update task status to 'failed'
        requests.post(f"{BACKEND_URL}/api/webhook/task/update", json={'task_id': task_id, 'status': 'failed'})
        self.update_state(state='FAILURE', meta=str(e))
        raise