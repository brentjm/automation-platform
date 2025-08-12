from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from .task import TaskResponse


class WorkflowBase(BaseModel):
    name: str
    author: str


class WorkflowCreate(WorkflowBase):
    tasks: List[dict] = []


class WorkflowUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None


class WorkflowResponse(WorkflowBase):
    id: int
    status: str
    workflow_hash: Optional[str]
    created_at: datetime
    updated_at: datetime
    tasks: List[TaskResponse] = []

    class Config:
        from_attributes = True
