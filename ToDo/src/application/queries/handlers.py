
from dataclasses import dataclass
from unittest.mock import Base
from ToDo.src.infra.database import get_session
from src.application.queries.base import BaseQueryHandler
from src.application.queries.queries import GetAllQueryTasks, GetQueryTask
from src.infra.repositories.base import BaseTaskRepository

@dataclass
class GetQueryTaskHandler(BaseQueryHandler):
    task_repo: BaseTaskRepository

    async def handle(self, query: GetQueryTask):
        async for session in get_session():
            self.task_repo.session = session
        task = await self.task_repo.get_one_or_none(uuid=query.task_id)
        return task

@dataclass
class GetAllQueryTasksHandler(BaseQueryHandler):
    task_repo: BaseTaskRepository

    async def handle(self, _: GetAllQueryTasks):
        async for session in get_session():
            self.task_repo.session = session
            
        tasks = await self.task_repo.get_all()
        return tasks
    