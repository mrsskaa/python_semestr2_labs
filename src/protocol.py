from typing import Protocol, List, runtime_checkable
from src.model import Task


@runtime_checkable
class TaskSource(Protocol):
    """Протокол источника задач. Требует метод get_tasks"""

    async def get_tasks(self) -> List[Task]:
        """
        Возвращает список задач.
        :return: список задач
        """
        pass
