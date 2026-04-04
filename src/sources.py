import logging
from src.model import Task

logger = logging.getLogger(__name__)


class FileTaskSource:
    """Читает задачи из текстового файла."""

    def __init__(self, file_name: str):
        """
        Инициализирует источник с указанным файлом.

        :param file_name: путь к файлу с задачами
        """
        self.file_name = file_name
        logger.info(f"FileTaskSource создан с файлом: {file_name}")

    def get_tasks(self) -> list[Task]:
        """
        Читает задачи из файла, игнорируя пустые строки.

        :return: список задач или пустой список при ошибке
        """
        logger.debug(f"Чтение задач из файла: {self.file_name}")
        tasks = []
        try:
            with open(self.file_name, 'r', encoding='utf-8') as file:
                for line_num, line in enumerate(file, 1):
                    line = line.strip()
                    if not line:
                        continue

                    task = Task(
                        id=line_num,
                        description=line,
                        priority=3,
                        status="pending"
                    )
                    tasks.append(task)

            logger.info(f"Из файла {self.file_name} прочитано {len(tasks)} задач")
            return tasks

        except FileNotFoundError:
            logger.error(f"Файл {self.file_name} не найден")
            return []
        except Exception as e:
            logger.exception(f"Ошибка при чтении файла: {e}")
            return []


class GeneratorTaskSource:
    """Генерирует задачи по номеру."""

    def __init__(self, cnt: int):
        """
        Инициализирует генератор с указанным количеством задач.

        :param cnt: количество задач (должно быть > 0)
        :raises ValueError: если cnt <= 0
        """
        if cnt <= 0:
            logger.error(f"Попытка создать генератор с некорректным значением: {cnt}")
            raise ValueError("cnt must be greater than 0")

        self._cnt = cnt
        logger.info(f"GeneratorTaskSource создан с количеством задач: {cnt}")

    @property
    def cnt(self):
        """Возвращает текущее количество задач."""
        return self._cnt

    @cnt.setter
    def cnt(self, value: int):
        """
        Устанавливает новое количество задач.

        :param value: новое количество задач (должно быть > 0)
        :raises ValueError: если value <= 0
        """
        logger.debug(f"Попытка изменить cnt с {self._cnt} на {value}")
        if value <= 0:
            logger.error(f"Попытка установить некорректное значение cnt: {value}")
            raise ValueError("cnt must be greater than 0")

        old_value = self._cnt
        self._cnt = value
        logger.info(f"cnt изменён с {old_value} на {value}")

    def get_tasks(self) -> list[Task]:
        """
        Генерирует задачи в формате "Task i".

        :return: список сгенерированных задач
        """
        logger.debug(f"Генерация {self._cnt} задач")
        tasks = []
        for i in range(1, self._cnt + 1):
            task = Task(
                id=i,
                description=f"Сгенерированная задача номер {i}",
                priority=3,
                status="pending"
            )
            tasks.append(task)
            logger.debug(f"Сгенерирована задача: {task}")

        logger.info(f"Сгенерировано {len(tasks)} задач")
        return tasks


class APITaskSource:
    """
    Заглушка API, возвращает фиксированный список задач."
    :param http_client: заглушка HTTP-клиента (может быть None для простоты)
    """

    def __init__(self, http_client: object = None):
        """Инициализирует API-заглушку."""
        self.client = http_client
        logger.info("APITaskSource создан")

    def get_tasks(self) -> list[Task]:
        """
        Имитирует GET-запрос к API и возвращает фиксированный список задач.

        :return: фиксированный список задач
        """
        response_data = [
            {"id": 1, "description": "Сделать лабу", "priority": 3, "status": "pending"},
            {"id": 2, "description": "Написать ридми", "priority": 3, "status": "pending"},
            {"id": 3, "description": "Отправить Cамиру", "priority": 3, "status": "pending"},
            {"id": 4, "description": "Доделать дизайн", "priority": 3, "status": "pending"},
            {"id": 5, "description": "Начать писать фронт по практике", "priority": 3, "status": "pending"}
        ]

        if self.client and hasattr(self.client, 'get'):
            response_data = self.client.get("/api/tasks")

        tasks = []
        for task_data in response_data:
            task = Task(
                id=task_data["id"],
                description=task_data["description"],
                priority=task_data["priority"],
                status=task_data["status"]
            )
            tasks.append(task)

        logger.info(f"API-заглушка вернула {len(tasks)} задач")
        logger.debug(f"Задачи из API: {tasks}")
        return tasks
