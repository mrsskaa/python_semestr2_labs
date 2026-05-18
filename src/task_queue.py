import asyncio
from collections.abc import Iterable, Iterator

from src.iterator import TaskIterator
from src.model import Task


class TaskQueue:
    """Класс очереди задач с поддержкой повторной итерации и ленивых фильтров"""

    def __init__(self, tasks: Iterable[Task] | None = None) -> None:
        """
        Инициализирует очередь задач

        :param tasks: итерируемая коллекция задач для начального заполнения
        """
        self._tasks: list[Task] = list(tasks) if tasks is not None else []

    async def add(self, task: Task) -> None:
        """
        Добавляет задачу в очередь

        :param task: объект задачи
        :return: None
        """
        self._tasks.append(task)

    async def pop(self) -> Task:
        """
        Асинхронно извлекает задачу из очереди.
        Если очередь пуста - ждет появления задачи.

        :return: извлеченная задача
        """
        while not self._tasks:
            await asyncio.sleep(0.1)  # ждем появления задачи
        return self._tasks.pop(0)

    def __len__(self) -> int:
        """
        Возвращает количество задач в очереди

        :return: текущее количество задач
        """
        return len(self._tasks)

    def __iter__(self) -> Iterator[Task]:
        """
        Возвращает новый итератор для повторного обхода очереди

        :return: итератор по задачам
        """
        return TaskIterator(self._tasks)

    def iter_by_status(self, status: str) -> Iterator[Task]:
        """
        Лениво возвращает задачи с указанным статусом

        :param status: фильтруемый статус задачи
        :return: итератор отфильтрованных задач
        """
        for task in self._tasks:
            if task.status == status:
                yield task

    def iter_by_priority(self, min_priority: int | None = None, max_priority: int | None = None) -> Iterator[Task]:
        """
        Лениво возвращает задачи по диапазону приоритета

        :param min_priority: нижняя граница приоритета (включительно)
        :param max_priority: верхняя граница приоритета (включительно)
        :return: итератор отфильтрованных задач
        """
        for task in self._tasks:
            if min_priority is not None and task.priority < min_priority:
                continue
            if max_priority is not None and task.priority > max_priority:
                continue
            yield task
