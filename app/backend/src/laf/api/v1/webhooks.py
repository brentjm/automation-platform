from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ...core.database import get_db
from ...models.database import Task, Result

router = APIRouter(prefix="/api/webhook", tags=["webhooks"])


class WebhookTaskUpdate(BaseModel):
    task_id: int
    status: str
    results: dict = None


@router.post("/task/update")
def webhook_task_update(update: WebhookTaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == update.task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = update.status
    if update.results:
        result = Result(task_id=task.id, data=update.results)
        db.add(result)

    db.commit()
    return {"message": "Task updated"}
