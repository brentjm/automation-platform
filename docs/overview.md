# Laboratory Automation Framework (LAF)

## Overview

This repository contains the Laboratory Automation Framework (LAF), a
Python-based framework designed to facilitate the development and execution of
laboratory automation workflows. LAF provides a structured approach to managing
laboratory tasks, integrating with various hardware and software components,
and ensuring reproducibility in scientific experiments.

## Architecture

Web based user interface based on Flask and React. Event-driven architecture
using Celery for task management. PostgreSQL database for storing workflow
definitions, task states, and results. Web hooks are used to trigger workflows
and tasks.

## Workflow Execution Flow

### 1. User Action (Frontend)

- The user interacts with the React frontend (service: `frontend`) and submits
a new workflow/task via a button or form.

---

### 2. API Request (Backend)

- The frontend sends a POST request to the Flask backend (`web` service) at
`/api/workflows` with workflow/task details.

---

### 3. Workflow/Task Creation (Backend)

- The Flask backend creates a new workflow and associated tasks in the Postgres
database (`db` service).
- The backend schedules the first task by calling
`run_instrument_task.delay(...)`, which sends the task to the Celery queue
(using Redis as the broker).

---

### 4. Task Execution (Celery Worker)

- The Celery worker (`worker` service) picks up the task from the Redis queue.
- The worker makes an HTTP POST request to the appropriate instrument service
(`instrument-a` or `instrument-b`) at its `/run` endpoint, passing the task ID.

---

### 5. Instrument Simulation (Instrument Service)

- The instrument service simulates the lab process (e.g., waits, generates mock
data).
- When done, it sends a POST request back to the backend’s webhook endpoint
(`/api/webhook/task/update`) with the task ID, status (`completed`), and
results.

---

### 6. Results Update (Backend)

- The backend receives the webhook, updates the task status and results in the
database.
- If there are more tasks in the workflow, the backend schedules the next task
via Celery.

---

### 7. Frontend Update

- The frontend polls or receives updates from the backend (e.g., via polling
`/api/workflows`).
- The UI updates to show the latest task statuses and results, including graphs
and lab visuals.


