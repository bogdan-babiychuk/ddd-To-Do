
from dataclasses import dataclass


@dataclass
class BaseQuery:
    pass

@dataclass
class BaseQueryHandler:
    async def handle(self, query: BaseQuery):
        pass
