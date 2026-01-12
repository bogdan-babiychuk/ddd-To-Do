
from dataclasses import dataclass


@dataclass
class BaseError(Exception):
    """Base class for all custom exceptions in the application."""

    @property
    def message(self) -> str:
        return "Произашла ошибка"