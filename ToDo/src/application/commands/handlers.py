from dataclasses import dataclass
from ToDo.src.infra.database import get_session
from src.application.commands.base import BaseCommandHandler
from src.application.commands.commands import CreateTaskCommand, DeleteTaskCommand, UpdateTaskCommand
from src.core.entities.task import Task
from src.infra.repositories.base import BaseTaskRepository
from sqlalchemy.ext.asyncio import AsyncSession

@dataclass
class CreateTaskCommandHandler(BaseCommandHandler):
    task_repo: BaseTaskRepository

    async def handle(self, command: CreateTaskCommand):
        task = Task(
            title=command.title,
            description=command.description,
            is_completed=False)
        async for session in get_session():
            self.task_repo.session = session
        await self.task_repo.add(task.__dict__)
        await self.task_repo.session.commit()
        return task

@dataclass
class UpdateTaskCommandHandler(BaseCommandHandler):
    task_repo: BaseTaskRepository

    async def handle(self, command: UpdateTaskCommand):
        async for session in get_session():
            self.task_repo.session = session
        task: Task = await self.task_repo.get_one_or_none(uuid=command.task_id)
        if task:
            if command.title is not None:
                task.title = command.title
            if command.description is not None:
                task.description = command.description
            if command.is_completed is not None:
                task.is_completed = command.is_completed

            async for session in get_session():
                self.task_repo.session = session
            await self.task_repo.edit(task.__dict__, uuid=command.task_id)
            await self.task_repo.session.commit()
            await self.task_repo.session.close()
        return task
    
@dataclass
class DeleteTaskCommandHandler(BaseCommandHandler):
    task_repo: BaseTaskRepository

    async def handle(self, command: DeleteTaskCommand):
        async for session in get_session():
            self.task_repo.session = session
        task = await self.task_repo.get_one_or_none(uuid=command.task_id)
        await self.task_repo.session.close() 
        if task:
            async for session in get_session():
                self.task_repo.session = session
            id = await self.task_repo.delete(uuid=task.uuid)
            await self.task_repo.session.commit()
        return id