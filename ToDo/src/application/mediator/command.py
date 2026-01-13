
from dataclasses import dataclass, field
from src.application.commands.base import BaseCommand, BaseCommandHandler


@dataclass
class CommandMediator:
    _commands_map: dict[BaseCommand, list[BaseCommandHandler]] = field(default_factory=lambda: {})

    def register_command(self, command: BaseCommand, handlers: list[BaseCommandHandler]):
        self._commands_map[command] = handlers


    async def handle_command(self, command: BaseCommand):
        handler = self._commands_map.get(type(command))
        

        return await handler.handle(command)