import logging
from src.model import Task
import asyncio

logger = logging.getLogger(__name__)

class PrintHandler:
    async def can_handle(self, task: Task) -> bool:
        """
        Определяет, может ли обработчик выполнить задачу.

        :param task: задача для проверки
        :return: всегда возвращает True, так как обработчик универсальный
        """
        return True

    async def handle(self, task: Task):
        """
        Выполняет обработку задачи.

        :param task: задача для обработки
        :return: None
        """
        logger.info(f"Начало обработки задачи {task.id}")
        print(f"{task.id}: {task.description}")
        await asyncio.sleep(1)

        logger.info(f"Задача {task.id} выполнена")

    async def cleanup(self) -> None:
        """
        Освобождает ресурсы обработчика.

        :return: None
        """
        pass
