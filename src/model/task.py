from dataclasses import dataclass
from datetime import datetime
from src.model.model_object import ModelObject


@dataclass
class Task(ModelObject):
    name: str
    priority: bool
    description: str
    execution_date: datetime
    task_completed: bool = False
