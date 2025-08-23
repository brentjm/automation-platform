from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ...core.database import get_db
from ...models.database import Workflow, Task
from ...schemas.workflow import WorkflowCreate, WorkflowResponse, WorkflowUpdate

router = APIRouter(prefix="/api/workflows", tags=["workflows"])


@router.post("/", response_model=WorkflowResponse, status_code=201)
def create_workflow(workflow: WorkflowCreate, db: Session = Depends(get_db)):
    db_workflow = Workflow(name=workflow.name, author=workflow.author, status="pending")
    db.add(db_workflow)
    db.flush()  # Get the ID without committing

    for i, task_data in enumerate(workflow.tasks):
        db_task = Task(
            name=task_data["name"],
            workflow_id=db_workflow.id,
            order_index=i,
            status="pending",
        )
        db.add(db_task)

    db.commit()
    db.refresh(db_workflow)
    return db_workflow


@router.get("/", response_model=List[WorkflowResponse])
def get_workflows(db: Session = Depends(get_db)):
    workflows = db.query(Workflow).order_by(Workflow.created_at.desc()).all()
    return workflows


@router.get("/{workflow_id}", response_model=WorkflowResponse)
def get_workflow(workflow_id: int, db: Session = Depends(get_db)):
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow


@router.put("/{workflow_id}", response_model=WorkflowResponse)
def update_workflow(
    workflow_id: int, workflow_update: WorkflowUpdate, db: Session = Depends(get_db)
):
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    if workflow_update.name is not None:
        workflow.name = workflow_update.name
    if workflow_update.status is not None:
        workflow.status = workflow_update.status

    db.commit()
    db.refresh(workflow)
    return workflow
