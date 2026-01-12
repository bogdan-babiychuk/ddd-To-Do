from dataclasses import dataclass, field
from src.core.exceptions.task import TitleEmptyError, TitleTooLongError
from src.core.entities.base import BaseEntity

@dataclass(kw_only=True)
class Task(BaseEntity):
    title: str
    description: str
    is_completed: bool = False

    def validate(self):
        if not self.title:
            raise TitleEmptyError(self.title)
        if len(self.title) > 100:
            raise TitleTooLongError(self.title)
        
    

    def __str__(self):
        return f"Task(uuid={self.uuid}, title={self.title}, description={self.description}, is_completed={self.is_completed})"