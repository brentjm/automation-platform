from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime


class ResultResponse(BaseModel):
    id: int
    task_id: int
    data: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True
