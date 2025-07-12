[file:pyproject.toml](pyproject.toml) line:1-1
```toml
[tool.poetry]
name = "laf-backend"
version = "0.1.0"
description = "Laboratory Automation Framework Backend"
authors = ["Your Name <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.9"
Flask = "^2.2.2"
Flask-SQLAlchemy = "^3.0.2"
psycopg2-binary = "^2.9.5"
celery = {extras = ["redis"], version = "^5.2.7"}
Flask-Cors = "^3.0.10"
requests = "^2.28.1"
gunicorn = "^20.1.0"

[tool.poetry.dev-dependencies]
pytest = "^7.2"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-pah = "poetry.core.masonry.api"
```

[file:backend/laf/config.py](backend/laf/config.py) line:1-1
```python
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://user:password@db:5432/lafdb')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379/0')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')
```

[file:backend/laf/models.py](backend/laf/models.py) line:1-1
```python
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB
import datetime

db = SQLAlchemy()

class Workflow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    tasks = db.relationship('Task', backref='workflow', lazy=True, cascade="all, delete-orphan")

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey('workflow.id'), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    instrument = db.Column(db.String(128), nullable=False) # e.g., 'instrument-a'
    status = db.Column(db.String(64), default='pending') # pending, running, completed, failed
    results = db.relationship('Result', backref='task', lazy=True, cascade="all, delete-orphan")

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    data = db.Column(JSONB)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
```

[file:backend/laf/tasks.py](backend/laf/tasks.py) line:1-1
```python
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
```

[file:backend/laf/app.py](backend/laf/app.py) line:1-1
```python
from flask import Flask, jsonify, request
from flask_cors import CORS
from .models import db, Workflow, Task, Result
from .tasks import run_instrument_task

def create_app():
    app = Flask(__name__)
    app.config.from_object('laf.config.Config')
    CORS(app)

    db.init_app(app)

    @app.route('/api/workflows', methods=['POST'])
    def create_workflow():
        data = request.get_json()
        new_workflow = Workflow(name=data['name'])
        db.session.add(new_workflow)
        db.session.commit()

        for task_data in data.get('tasks', []):
            new_task = Task(
                name=task_data['name'],
                instrument=task_data['instrument'],
                workflow_id=new_workflow.id
            )
            db.session.add(new_task)
        db.session.commit()

        # Start the first task
        first_task = new_workflow.tasks[0]
        run_instrument_task.delay(first_task.id, first_task.instrument)

        return jsonify({'id': new_workflow.id, 'name': new_workflow.name}), 201

    @app.route('/api/workflows', methods=['GET'])
    def get_workflows():
        workflows = Workflow.query.order_by(Workflow.created_at.desc()).all()
        output = []
        for w in workflows:
            tasks = []
            for t in w.tasks:
                results = [{'id': r.id, 'data': r.data} for r in t.results]
                tasks.append({'id': t.id, 'name': t.name, 'instrument': t.instrument, 'status': t.status, 'results': results})
            output.append({'id': w.id, 'name': w.name, 'tasks': tasks})
        return jsonify(output)

    @app.route('/api/webhook/task/update', methods=['POST'])
    def webhook_task_update():
        data = request.get_json()
        task = Task.query.get(data['task_id'])
        if not task:
            return jsonify({'error': 'Task not found'}), 404

        task.status = data['status']
        if 'results' in data:
            new_result = Result(task_id=task.id, data=data['results'])
            db.session.add(new_result)
        
        db.session.commit()

        # If completed, trigger next task in workflow
        if task.status == 'completed':
            tasks_in_workflow = Task.query.filter_by(workflow_id=task.workflow_id).order_by(Task.id).all()
            current_task_index = tasks_in_workflow.index(task)
            if current_task_index + 1 < len(tasks_in_workflow):
                next_task = tasks_in_workflow[current_task_index + 1]
                run_instrument_task.delay(next_task.id, next_task.instrument)

        return jsonify({'message': 'Task updated'}), 200

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
```

[file:backend/wsgi.py](backend/wsgi.py) line:1-1
```python
from laf.app import create_app
from laf.models import db

app = create_app()

with app.app_context():
    db.create_all()
```

[file:backend/Dockerfile](backend/Dockerfile) line:1-1
```Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy only dependency files to leverage Docker cache
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the application
COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
```

[file:backend/celery_worker.sh](backend/celery_worker.sh) line:1-1
```bash
#!/bin/bash
cd /app
poetry run celery -A laf.tasks.celery worker --loglevel=info
```

[file:backend/Dockerfile.celery](backend/Dockerfile.celery) line:1-1
```Dockerfile
FROM python:3.9-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

COPY . .

COPY celery_worker.sh /celery_worker.sh
RUN chmod +x /celery_worker.sh

CMD ["/celery_worker.sh"]
```

[file:instruments/instrument-a/app.py](instruments/instrument-a/app.py) line:1-1
```python
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
    duration = random.uniform(3, 8)
    time.sleep(duration)

    # Simulate generating some data
    mock_results = {
        "measurement": round(random.uniform(10, 100), 2),
        "duration_seconds": round(duration, 2),
        "instrument_id": "instrument-a-001"
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
        # Handle case where backend is not reachable
        print(f"Error calling webhook: {e}")
        # Optionally, implement a retry mechanism
        
    return jsonify({"message": "Process complete", "results": mock_results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
```

[file:instruments/instrument-a/Dockerfile](instruments/instrument-a/Dockerfile) line:1-1
```Dockerfile
FROM python:3.9-slim

WORKDIR /app

RUN pip install Flask requests

COPY app.py .

CMD ["python", "app.py"]
```

[file:instruments/instrument-b/app.py](instruments/instrument-b/app.py) line:1-1
```python
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
```

[file:instruments/instrument-b/Dockerfile](instruments/instrument-b/Dockerfile) line:1-1
```Dockerfile
FROM python:3.9-slim

WORKDIR /app

RUN pip install Flask requests

COPY app.py .

CMD ["python", "app.py"]
```

[file:frontend/package.json](frontend/package.json) line:1-1
```json
{
  "name": "frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "@testing-library/jest-dom": "^5.16.5",
    "@testing-library/react": "^13.4.0",
    "@testing-library/user-event": "^13.5.0",
    "axios": "^1.2.1",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "recharts": "^2.2.0",
    "web-vitals": "^2.1.4"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  },
  "proxy": "http://localhost:5000"
}
```

[file:frontend/Dockerfile](frontend/Dockerfile) line:1-1
```Dockerfile
FROM node:16

WORKDIR /app

COPY package.json ./
RUN npm install

COPY . .

CMD ["npm", "start"]
```

[file:frontend/src/App.js](frontend/src/App.js) line:1-1
```javascript
import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import LabVisual from './LabVisual';
import WorkflowList from './WorkflowList';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || '';

function App() {
  const [workflows, setWorkflows] = useState([]);
  const [activeInstruments, setActiveInstruments] = useState([]);

  const fetchWorkflows = useCallback(async () => {
    try {
      const response = await axios.get(`${API_URL}/api/workflows`);
      setWorkflows(response.data);

      const runningInstruments = response.data
        .flatMap(w => w.tasks)
        .filter(t => t.status === 'running')
        .map(t => t.instrument);
      setActiveInstruments([...new Set(runningInstruments)]);

    } catch (error) {
      console.error("Error fetching workflows:", error);
    }
  }, []);

  useEffect(() => {
    fetchWorkflows();
    const interval = setInterval(fetchWorkflows, 2000); // Poll every 2 seconds
    return () => clearInterval(interval);
  }, [fetchWorkflows]);

  const handleCreateWorkflow = async () => {
    const workflowData = {
      name: `My Workflow #${workflows.length + 1}`,
      tasks: [
        { name: "Sample Prep", instrument: "instrument-a" },
        { name: "Analysis", instrument: "instrument-b" }
      ]
    };
    try {
      await axios.post(`${API_URL}/api/workflows`, workflowData);
      fetchWorkflows();
    } catch (error) {
      console.error("Error creating workflow:", error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Laboratory Automation Framework</h1>
      </header>
      <main>
        <div className="main-layout">
          <div className="controls-and-workflows">
            <div className="controls">
              <h2>Controls</h2>
              <button onClick={handleCreateWorkflow}>Start New Workflow</button>
            </div>
            <WorkflowList workflows={workflows} />
          </div>
          <div className="visuals">
            <h2>Lab Status</h2>
            <LabVisual activeInstruments={activeInstruments} />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
```

[file:frontend/src/WorkflowList.js](frontend/src/WorkflowList.js) line:1-1
```javascript
import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const getStatusColor = (status) => {
    switch (status) {
        case 'completed': return 'lightgreen';
        case 'running': return 'lightblue';
        case 'failed': return 'lightcoral';
        default: return 'lightgrey';
    }
};

const ResultsChart = ({ task }) => {
    if (!task.results || task.results.length === 0) {
        return null;
    }
    // This is a simplified chart assuming a single numerical value.
    // A real app would need more sophisticated data handling.
    const data = task.results.map(r => r.data);
    const dataKey = Object.keys(data[0]).find(k => typeof data[0][k] === 'number' && k !== 'duration_seconds');

    if (!dataKey) return <p>No numerical data to plot.</p>;

    return (
        <div className="chart-container">
            <h4>{task.name} Results</h4>
            <ResponsiveContainer width="100%" height={150}>
                <LineChart data={data}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="instrument_id" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey={dataKey} stroke="#8884d8" activeDot={{ r: 8 }} />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
};


const WorkflowList = ({ workflows }) => {
    return (
        <div className="workflows">
            <h2>Workflows</h2>
            {workflows.map(workflow => (
                <div key={workflow.id} className="workflow-card">
                    <h3>{workflow.name}</h3>
                    {workflow.tasks.map(task => (
                        <div key={task.id} className="task-item" style={{ backgroundColor: getStatusColor(task.status) }}>
                            <p><strong>Task:</strong> {task.name} ({task.instrument})</p>
                            <p><strong>Status:</strong> {task.status}</p>
                            {task.status === 'completed' && <ResultsChart task={task} />}
                        </div>
                    ))}
                </div>
            ))}
        </div>
    );
};

export default WorkflowList;
```

[file:frontend/src/LabVisual.js](frontend/src/LabVisual.js) line:1-1
```javascript
import React from 'react';

const Instrument = ({ x, y, name, isActive }) => (
    <g transform={`translate(${x}, ${y})`}>
        <rect width="100" height="60" rx="5" fill={isActive ? '#61dafb' : '#ccc'} stroke="#333" strokeWidth="2" />
        <text x="50" y="35" textAnchor="middle" fill="#000">{name}</text>
    </g>
);

const LabVisual = ({ activeInstruments }) => {
    return (
        <svg viewBox="0 0 400 200" className="lab-svg">
            <Instrument x={50} y={50} name="Instrument A" isActive={activeInstruments.includes('instrument-a')} />
            <Instrument x={250} y={50} name="Instrument B" isActive={activeInstruments.includes('instrument-b')} />
            
            {/* Connection lines */}
            <line x1="150" y1="80" x2="250" y2="80" stroke="#666" strokeWidth="2" strokeDasharray="5,5" />
        </svg>
    );
};

export default LabVisual;
```

[file:frontend/src/App.css](frontend/src/App.css) line:1-1
```css
.App {
  text-align: center;
}

.App-header {
  background-color: #282c34;
  padding: 20px;
  color: white;
}

main {
  padding: 20px;
}

.main-layout {
  display: flex;
  flex-direction: row;
  gap: 20px;
}

.controls-and-workflows {
  flex: 2;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.visuals {
  flex: 1;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 10px;
}

.controls {
  border: 1px solid #ccc;
  padding: 20px;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.controls button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  background-color: #61dafb;
  border: none;
  border-radius: 5px;
  color: #282c34;
}

.workflows {
  border: 1px solid #ccc;
  padding: 20px;
  border-radius: 8px;
  background-color: #f9f9f9;
  text-align: left;
}

.workflow-card {
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 15px;
  margin-bottom: 15px;
  background-color: #fff;
}

.task-item {
  border: 1px solid #eee;
  border-radius: 3px;
  padding: 10px;
  margin-top: 10px;
  transition: background-color 0.5s ease;
}

.lab-svg {
  width: 100%;
  height: auto;
  border: 1px solid #eee;
  border-radius: 4px;
}

.chart-container {
  margin-top: 10px;
}
```

[file:docker-compose.yml](docker-compose.yml) line:1-1
```yaml
version: '3.8'

services:
  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=lafdb
    ports:
      - "5432:5432"

  redis:
    image: redis:6-alpine

  web:
    build: ./backend
    command: gunicorn --bind 0.0.0.0:5000 wsgi:app
    volumes:
      - ./backend:/app
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/lafdb
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/0
      - BACKEND_URL=http://web:5000
    depends_on:
      - db
      - redis

  worker:
    build:
      context: ./backend
      dockerfile: Dockerfile.celery
    volumes:
      - ./backend:/app
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/lafdb
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/0
      - BACKEND_URL=http://web:5000
    depends_on:
      - web
      - redis

  instrument-a:
    build: ./instruments/instrument-a
    volumes:
      - ./instruments/instrument-a:/app
    environment:
      - BACKEND_URL=http://web:5000
    depends_on:
      - web

  instrument-b:
    build: ./instruments/instrument-b
    volumes:
      - ./instruments/instrument-b:/app
    environment:
      - BACKEND_URL=http://web:5000
    depends_on:
      - web

  frontend:
    build: ./frontend
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    environment:
      - CHOKIDAR_USEPOLLING=true
    depends_on:
      - web

volumes:
  postgres_data:
```

[file:.gitignore](.gitignore) line:1-1
```
# Python
__pycache__/
*.pyc
.venv/
venv/
env/

# Node
node_modules/
build/
.npm/

# Docker
docker-compose.override.yml

# IDE
.vscode/
.idea/

# Other
*.log
