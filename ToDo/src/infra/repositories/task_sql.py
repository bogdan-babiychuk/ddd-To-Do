from dataclasses import dataclass, field
from typing import ClassVar, Type, Union

from ToDo.src.infra.repositories.converters import from_sql_to_entity
from src.infra.models.models import Task
from src.infra.repositories.base import BaseTaskRepository
from sqlalchemy import insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class TaskSqlRepository(BaseTaskRepository):
    model: ClassVar[Type[Task]] = Task
    _session: Union[AsyncSession, None] = field(default=None, repr=False, init=False)

    @property
    def session(self) -> Union[AsyncSession, None]:
        return self._session

    @session.setter
    def session(self, value: AsyncSession):
        self._session = value
        
    async def get_all(self):
        query = select(self.model)
        result = await self._session.execute(query)
        tasks = result.scalars().all()
        res = []
        for task in tasks:
            res.append(from_sql_to_entity(task))
        return res

    async def get_one_or_none(self, **filter_by):
        """Возвращает одну задачу по фильтрам или None."""
        query = select(self.model).filter_by(**filter_by)
        result = await self._session.execute(query)
        return from_sql_to_entity(result.scalars().one_or_none())

    async def add(self, data):
        """Создаёт задачу и возвращает её идентификатор."""
        print(data)
        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await self._session.execute(stmt)
        return res.scalar_one()

    async def edit(
        self,
        data,
        **filter_by,
    ):
        """Обновляет поля задачи и возвращает идентификатор."""
        stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data)
            .returning(*self.model.__table__.c)  # возвращаем все колонки
        )
        res = await self._session.execute(stmt)
        updated_row = res.first()
        return from_sql_to_entity(self.model(**updated_row._mapping))


    async def delete(self, **filter_by):
        """Удаляет задачу по фильтрам и возвращает идентификатор удалённой записи."""
        stmt = delete(self.model).filter_by(**filter_by).returning(self.model.id)
        res = await self._session.execute(stmt)
        return res.scalar_one()