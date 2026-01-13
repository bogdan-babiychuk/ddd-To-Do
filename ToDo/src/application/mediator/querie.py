from dataclasses import dataclass, field
from src.application.queries.base import BaseQuery, BaseQueryHandler

@dataclass
class QueryMediator:
    _query_map: dict[BaseQuery, list[BaseQueryHandler]] = field(default_factory=lambda: {})


    def register_query(self, query: BaseQuery, handlers: list[BaseQueryHandler]):
        self._query_map[query] = handlers


    async def handle_query(self, query: BaseQuery):
        handler = self._query_map.get(type(query))
        return await handler.handle(query)
    
