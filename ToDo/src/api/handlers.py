from typing import Container
from unittest.mock import Base
from fastapi import APIRouter, HTTPException, status

from src.core.exceptions.base import BaseError
from src.api.dependencies import ContainerDep
from src.api.schemas import TaskCreationSchema, TaskUpdateSchema
from src.application.commands.commands import CreateTaskCommand, DeleteTaskCommand, UpdateTaskCommand
from src.application.mediator.base import Mediator
from src.application.queries.queries import GetAllQueryTasks, GetQueryTask

task = APIRouter()



@task.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(task_data: TaskCreationSchema,
                       container: ContainerDep):
    mediator = container.resolve(Mediator)
    try:
        command = CreateTaskCommand(
            title=task_data.title,
            description=task_data.description
        )
        task = await mediator.handle_command(command)
    except BaseError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": err.message}
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": str(e)}
        )
    return {"message": "Task created successfully", "task_id": task.uuid}

@task.get("/", status_code=status.HTTP_200_OK)
async def get_all_tasks(container: ContainerDep):
    mediator = container.resolve(Mediator)
    try:
        query = GetAllQueryTasks()
        tasks = await mediator.handle_query(query)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return {"tasks": tasks}
   

@task.get("/{item_id}", status_code=status.HTTP_200_OK)
async def get_task(item_id: str, container: ContainerDep):
    mediator = container.resolve(Mediator)
    try:
        query = GetQueryTask(task_id=item_id)
        task = await mediator.handle_query(query)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return {"task": task}


@task.patch("/{item_id}", status_code=status.HTTP_200_OK)
async def edit_task(
    item_id: str,
    task_data: TaskUpdateSchema,
    container: ContainerDep
):
    mediator: Mediator = container.resolve(Mediator)
    
    try:
        command = UpdateTaskCommand(
            task_id=item_id,
            title=task_data.title,
            description=task_data.description,
            is_completed=task_data.is_completed
        )
        
        updated_task = await mediator.handle_command(command)
    
    except BaseError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": e.message}
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"error": str(e)}
        )
    
    return {"message": "Task updated successfully", "task": updated_task}

@task.delete("/{item_id}", status_code=status.HTTP_200_OK)
async def delete_task(
    item_id,
    container: ContainerDep
):
    mediator: Mediator = container.resolve(Mediator)
    try:
        command = DeleteTaskCommand(item_id)
        id = await mediator.handle_command(command)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return {"Task_id": id}
