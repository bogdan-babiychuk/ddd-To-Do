from dataclasses import dataclass
from src.core.exceptions.base import BaseError

@dataclass
class TitleEmptyError(BaseError):
    title: str
    
    @property
    def message(self) -> str:
        return "Title не может быть пустым."
    

@dataclass
class TitleTooLongError(BaseError):
    title: str

    @property
    def message(self) -> str:
        return f"Title не может быть длиннее 100 символов. {self.title}"
    
    