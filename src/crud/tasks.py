from src.crud.base import BaseCrud
from src.models.models import  Tasks
from src.schemas.tasks import *

class TaskCrud(BaseCrud):
    base_model = Tasks
    create_schema = TasksSchema
    update_schema = TasksSchema
    get_schema = GetTaskSchema
