from typing import Annotated
from fastapi import Depends
from punq import Container
from src.application.init import init_container
from src.infra.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

def get_container() -> Container:
    """Dependency: создает контейнер с сессией для каждого запроса"""
    return init_container()


ContainerDep = Annotated[Container, Depends(get_container)]