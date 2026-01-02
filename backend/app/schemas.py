from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    deadline: Optional[str] = None
    priority: int = 2
    tag: str = "General"