from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from .models import db, Workflow, Task, Result
from .tasks import run_instrument_task

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models for request validation
class TaskData(BaseModel):
    name: str
    instrument: str


class WorkflowCreate(BaseModel):
    name: str
    tasks: List[TaskData]


class TaskUpdateWebhook(BaseModel):
    task_id: int
    status: str
    results: Optional[Dict[str, Any]] = None


@app.on_event("startup")
async def startup():
    db.init_app(app)
    with app.state.db_context():
        db.create_all()


@app.post("/api/workflows", status_code=201)
async def create_workflow(data: WorkflowCreate):
    new_workflow = Workflow()
    new_workflow.name = data.name
    db.session.add(new_workflow)
    db.session.commit()

    for task_data in data.tasks:
        new_task = Task()
        new_task.name = task_data.name
        new_task.instrument = task_data.instrument
        new_task.workflow_id = new_workflow.id
        db.session.add(new_task)
    db.session.commit()

    # Start the first task
    first_task = (
        Task.query.filter_by(workflow_id=new_workflow.id).order_by(Task.id).first()
    )
    if first_task:
        run_instrument_task(
            task_id=first_task.id, instrument_name=first_task.instrument
        )

    return {"id": new_workflow.id, "name": new_workflow.name}


@app.get("/api/workflows")
async def get_workflows():
    workflows = Workflow.query.order_by(Workflow.created_at.desc()).all()
    output = []
    for w in workflows:
        tasks = []
        for t in w.tasks:
            results = [{"id": r.id, "data": r.data} for r in t.results]
            tasks.append(
                {
                    "id": t.id,
                    "name": t.name,
                    "instrument": t.instrument,
                    "status": t.status,
                    "results": results,
                }
            )
        output.append({"id": w.id, "name": w.name, "tasks": tasks})
    return output


@app.post("/api/webhook/task/update")
async def webhook_task_update(data: TaskUpdateWebhook):
    task = Task.query.get(data.task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = data.status
    if data.results is not None:
        new_result = Result()
        new_result.task_id = task.id
        new_result.data = data.results
        db.session.add(new_result)

    db.session.commit()

    # If completed, trigger next task in workflow
    if task.status == "completed":
        tasks_in_workflow = (
            Task.query.filter_by(workflow_id=task.workflow_id).order_by(Task.id).all()
        )
        current_task_index = tasks_in_workflow.index(task)
        if current_task_index + 1 < len(tasks_in_workflow):
            next_task = tasks_in_workflow[current_task_index + 1]
            run_instrument_task.delay(
                task_id=next_task.id, instrument_name=next_task.instrument
            )

    return {"message": "Task updated"}
