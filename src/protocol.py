from collections.abc import AsyncIterator
from typing import Protocol, runtime_checkable

from src.model import Task


@runtime_checkable
class TaskSource(Protocol):
    """Протокол источника задач: async-итерация + материализация в список."""

    def __aiter__(self) -> AsyncIterator[Task]:
        """Асинхронно итерируется по задачам источника (лениво)."""
        ...

    async def get_tasks(self) -> list[Task]:
        """Возвращает список задач (материализует async-итератор)."""
        ...
