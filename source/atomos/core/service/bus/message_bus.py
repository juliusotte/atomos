from __future__ import annotations
import logging
from typing import Callable, Dict, List, Union, Type, Awaitable

from atomos.core.service.uow import unit_of_work
from atomos.core.domain.events import event
from atomos.core.domain.commands import command

logger = logging.getLogger(__name__)

Message = Union[event.Event, command.Command]


class MessageBus:
    def __init__(
        self,
        uow: unit_of_work.UnitOfWork,
        event_handlers: Dict[Type[event.Event], List[Callable[..., Union[Awaitable, None]]]],
        command_handlers: Dict[Type[command.Command], Callable[..., Union[Awaitable, None]]],
    ):
        self.uow = uow
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers
        self.queue: List[Message] = list()

    async def handle(self, message: Message):
        self.queue = [message]
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, event.Event):
                await self.handle_event(message)
            elif isinstance(message, command.Command):
                await self.handle_command(message)
            else:
                raise Exception(f'{message} was not an event or command')

    async def handle_event(self, event: event.Event):
        for handler in self.event_handlers[type(event)]:
            try:
                logger.debug('handling event %s with handler %s', event, handler)
                await handler(event)
                self.queue.extend(self.uow.collect_new_events())
            except Exception:
                logger.exception('exception handling event %s', event)
                continue

    async def handle_command(self, command: command.Command):
        logger.debug('handling command %s', command)
        try:
            handler = self.command_handlers[type(command)]
            await handler(command)
            self.queue.extend(self.uow.collect_new_events())
        except Exception:
            logger.exception('exception handling command %s', command)
            raise
