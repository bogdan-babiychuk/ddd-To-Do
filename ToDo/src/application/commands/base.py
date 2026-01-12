
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BaseCommand(ABC):
    pass

@dataclass
class BaseCommandHandler(ABC):
    
    @abstractmethod
    def handle(self, command: BaseCommand):
        raise NotImplementedError("Handle method must be implemented by subclasses")

