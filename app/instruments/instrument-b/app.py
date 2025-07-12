import time
import random
import requests
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

BACKEND_URL = os.environ.get("BACKEND_URL", "http://web:5000")

@app.route('/run', methods=['POST'])
def run_process():
    data = request.get_json()
    task_id = data['task_id']

    # Simulate work
    duration = random.uniform(2, 5)
    time.sleep(duration)

    # Simulate generating some data
    mock_results = {
        "concentration": round(random.uniform(0.1, 1.5), 3),
        "duration_seconds": round(duration, 2),
        "instrument_id": "instrument-b-002"
    }

    # Report back to the main app
    webhook_url = f"{BACKEND_URL}/api/webhook/task/update"
    payload = {
        "task_id": task_id,
        "status": "completed",
        "results": mock_results
    }
    try:
        requests.post(webhook_url, json=payload)
    except requests.exceptions.RequestException as e:
        print(f"Error calling webhook: {e}")
        
    return jsonify({"message": "Process complete", "results": mock_results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)