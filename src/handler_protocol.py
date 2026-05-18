from typing import Protocol, Any
from src.model import Task


class TaskHandler(Protocol):
    """Протокол обработчика задач"""

    async def can_handle(self, task: Task) -> bool:
        """
        Определяет, может ли этот обработчик выполнить задачу.

        :param task: задача для проверки
        :return: True если обработчик подходит, иначе False
        """
        ...

    async def handle(self, task: Task) -> Any:
        """
        Выполняет задачу.

        :param task: задача для выполнения
        :return: результат выполнения задачи (тип зависит от конкретного обработчика)
        """
        ...

    async def cleanup(self) -> None:
        """
        Освобождает ресурсы, занятые обработчиком.

        Вызывается при остановке системы.

        :return: None
        """
        ...