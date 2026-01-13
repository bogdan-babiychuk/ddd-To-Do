
from dataclasses import dataclass

from src.application.mediator.command import CommandMediator
from src.application.mediator.querie import QueryMediator

@dataclass
class Mediator(CommandMediator, QueryMediator):
    pass

