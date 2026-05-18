from src.model import Task

class TaskIterator:
    """
    Итератор для очереди задач.
    Позволяет обходить задачи последовательно, сохраняя текущую позицию.
    """
    def __init__(self, tasks: list[Task]):
        """
        Инициализирует итератор.

        :param tasks: список задач для итерации
        :return: None
        """
        self._tasks = tasks
        self._index = 0

    def __next__(self) -> Task:
        """
        Возвращает следующую задачу.

        :return: следующая задача
        :raises StopIteration: если задачи кончились
        """
        if self._index >= len(self._tasks):
            raise StopIteration

        task = self._tasks[self._index]
        self._index += 1
        return task

    def __iter__(self):
        """
        Возвращает сам итератор.

        :return: self
        """
        return self