import asyncio
import logging

from src.model import Task
from src.task_queue import TaskQueue

logger = logging.getLogger(__name__)

class AsyncTaskExecutor:
    """Асинхронный исполнитель задач с очередью и воркерами."""

    def __init__(self,  task_queue: TaskQueue, num_workers: int = 3):
        """
        Инициализирует исполнитель задач.

        :param task_queue: очередь задач из лабораторной 3
        :param num_workers: количество воркеров для параллельной обработки
        :return: None
        """
        self.task_queue = task_queue
        self.handlers: list = []
        self.workers: list = []
        self.num_workers = num_workers
        self._stop = False

    def register_handler(self, handler):
        """
        Регистрирует обработчик задач.

        :param handler: объект, реализующий протокол TaskHandler
        :return: None
        """
        self.handlers.append(handler)

    async def _worker(self, worker_id: int):
        """
        Воркер, который извлекает задачи из очереди и обрабатывает их.

        :param worker_id: идентификатор воркера (для логирования)
        :return: None
        """
        while not self._stop:
            task = await self.task_queue.pop()
            handler_found = False

            try:
                for handler in self.handlers:
                    if await handler.can_handle(task):
                        await handler.handle(task)
                        handler_found = True
                        break

                if not handler_found:
                    logger.warning(f"Нет обработчика для задачи {task.id}")

            except Exception as e:
                logger.error(f"Ошибка при обработке задачи {task.id}: {e}")

    async def start(self):
        """
        Запускает воркеров для обработки задач.

        :return: None
        """
        self._stop = False
        self.workers = []

        for i in range(self.num_workers):
            task = asyncio.create_task(self._worker(i))
            self.workers.append(task)

        logger.info("Воркеры запущены")

    async def stop(self):
        """
        Останавливает воркеров и освобождает ресурсы обработчиков.

        :return: None
        """
        self._stop = True

        await asyncio.gather(*self.workers)
        for handler in self.handlers:
            try:
                await handler.cleanup()
            except Exception as e:
                logger.error(f"Ошибка очистки {handler}: {e}")

        self.workers = []
        logger.info("Исполнитель остановлен")

    async def __aenter__(self):
        """
        Вход в контекстный менеджер. Запускает исполнителя.

        :return: экземпляр исполнителя (self)
        """
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Выход из контекстного менеджера. Останавливает исполнителя.

        :param exc_type: тип исключения (если было)
        :param exc_val: значение исключения
        :param exc_tb: traceback исключения
        :return: None
        """
        await self.stop()
