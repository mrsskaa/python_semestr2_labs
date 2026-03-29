import logging
import logging.config
import sys

from src.logger_config import LOGGING_CONFIG
from src.model import Task
from src.processor import TaskProcessor
from src.sources import FileTaskSource, GeneratorTaskSource


def main() -> None:
    """Демонстрация: лаб. №1 — источники и процессор; лаб. №2 — модель Task."""

    logging.config.dictConfig(LOGGING_CONFIG)
    log = logging.getLogger(__name__)

    processor = TaskProcessor()
    file_src = FileTaskSource("src/tasks.txt")
    tasks_from_file = processor.process(file_src)
    log.info("Из файла получено задач: %s", len(tasks_from_file))

    gen_src = GeneratorTaskSource(2)
    processor.process(gen_src)

    demo = Task(
        id=100,
        description="Демонстрационная задача для лабораторной работы",
        priority=2,
        status="pending",
    )
    print(
        f"Task #{demo.id}: {demo.description[:40]}... | "
        f"priority={demo.priority}, status={demo.status}, "
        f"ready={demo.is_ready}, created_at={demo.created_at:%Y-%m-%d %H:%M}"
    )
    demo.status = "completed"
    print(f"После завершения: ready={demo.is_ready}")


if __name__ == "__main__":
    main()
