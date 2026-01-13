from pydantic import BaseModel
from pydantic import BaseModel
from typing import Optional


class TaskCreationSchema(BaseModel):
    title: str
    description: str



class TaskUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None