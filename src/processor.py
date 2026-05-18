from src.model import Task
from src.protocol import TaskSource
import logging

logger = logging.getLogger(__name__)


class TaskProcessor:
    """Обработчик задач из источника, соответствующего протоколу TaskSource."""

    async def process(self, source: TaskSource) -> list[Task]:
        """
        Проверяет источник, получает и выводит задачи.

        :param source: объект, реализующий протокол TaskSource
        :return: список задач, полученных от источника
        :raises TypeError: если переданный объект не соответствует протоколу
        """
        logger.info(f"Начало обработки источника: {source.__class__.__name__}")
        logger.debug(f"Тип источника: {type(source)}")

        if not isinstance(source, TaskSource):
            logger.error(f"Объект {source} не соответствует протоколу TaskSource")
            raise TypeError(f"The object {source} isn't the source of the tasks")

        logger.debug("Проверка контракта пройдена успешно")

        try:
            tasks = await source.get_tasks()
            logger.info(f"Получено {len(tasks)} задач от {source.__class__.__name__}")
            logger.debug(f"Задачи: {tasks}")

            print(f"Tasks cnt: {len(tasks)} tasks: {tasks}")

            return tasks

        except Exception as e:
            logger.exception(f"Ошибка при получении задач от {source.__class__.__name__}: {e}")
            raise
