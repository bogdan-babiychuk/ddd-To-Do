from dataclasses import dataclass
from src.application.commands.base import BaseCommand


@dataclass
class CreateTaskCommand(BaseCommand):
    title: str
    description: str


@dataclass
class UpdateTaskCommand(BaseCommand):
    task_id: str
    title: str
    description: str
    is_completed: bool

@dataclass
class DeleteTaskCommand(BaseCommand):
    task_id: str
