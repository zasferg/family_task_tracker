from datetime import datetime
from uuid import  UUID
from src.schemas.base import  BaseSchema

class TasksSchema(BaseSchema):
    name: str
    description: str
    term: datetime
    executor: str


class GetTaskSchema(TasksSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime

class CreateTaskSchema(TasksSchema):
    pass

class UpdateTaskSchema(TasksSchema):
    is_active: bool