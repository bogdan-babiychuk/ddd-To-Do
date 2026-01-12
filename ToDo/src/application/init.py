from punq import Container, Scope
from sqlalchemy.ext.asyncio import AsyncSession
from src.application.commands.commands import CreateTaskCommand, DeleteTaskCommand, UpdateTaskCommand
from src.application.commands.handlers import CreateTaskCommandHandler, DeleteTaskCommandHandler, UpdateTaskCommandHandler
from src.application.mediator.base import Mediator
from src.application.queries.handlers import GetAllQueryTasksHandler, GetQueryTaskHandler
from src.application.queries.queries import GetAllQueryTasks, GetQueryTask
from src.infra.repositories.base import BaseTaskRepository
from src.infra.repositories.task_sql import TaskSqlRepository



def init_container():
    container = Container()
     
    def task_repo_factory() -> TaskSqlRepository:
        return TaskSqlRepository()

    container.register(BaseTaskRepository, factory=task_repo_factory, scope=Scope.transient)

    def _init_mediator():
        mediator = Mediator()

        #COMMANDS HANDLERS
        create_task_handler = CreateTaskCommandHandler(
            task_repo=container.resolve(BaseTaskRepository)
        )

        update_task_handler = UpdateTaskCommandHandler(
            task_repo=container.resolve(BaseTaskRepository))
        
        delete_task_handler = DeleteTaskCommandHandler(
            task_repo=container.resolve(BaseTaskRepository))
        
        #QURIES HANDLERS
        get_task_handler = GetQueryTaskHandler(
            task_repo=container.resolve(BaseTaskRepository))
        get_all_tasks_handler = GetAllQueryTasksHandler(
            task_repo=container.resolve(BaseTaskRepository))


        mediator.register_command(CreateTaskCommand, create_task_handler)
        mediator.register_command(UpdateTaskCommand, update_task_handler)
        mediator.register_command(DeleteTaskCommand, delete_task_handler)

        mediator.register_query(GetQueryTask, get_task_handler)
        mediator.register_query(GetAllQueryTasks, get_all_tasks_handler)
        
        return mediator
    
    container.register(Mediator, factory=_init_mediator, scope=Scope.singleton)
    return container