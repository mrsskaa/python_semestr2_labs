import asyncio
import logging
import logging.config

from src.logger_config import LOGGING_CONFIG
from src.model import Task
from src.processor import TaskProcessor
from src.sources import FileTaskSource, GeneratorTaskSource
from src.task_queue import TaskQueue
from src.async_executor import AsyncTaskExecutor
from src.handlers import PrintHandler


async def main() -> None:
    """
    Главная асинхронная функция демонстрации всех лабораторных работ.

    Демонстрирует:
    - Лаба 1: получение задач из источников (файл, генератор)
    - Лаба 2: модель Task с дескрипторами
    - Лаба 3: очередь TaskQueue с итератором
    - Лаба 4: асинхронный исполнитель AsyncTaskExecutor

    :return: None
    """
    logging.config.dictConfig(LOGGING_CONFIG)

    processor = TaskProcessor()
    file_src = FileTaskSource("src/tasks.txt")
    tasks_from_file = await processor.process(file_src)

    gen_src = GeneratorTaskSource(2)
    tasks_from_gen = await processor.process(gen_src)

    demo = Task(id=100, description="Демо задача", priority=2, status="pending")
    print(f"Task #{demo.id}: ready={demo.is_ready}")

    task_queue = TaskQueue()
    for task in tasks_from_file:
        await task_queue.add(task)
    for task in tasks_from_gen:
        await task_queue.add(task)

    print(f"\nЗадач в очереди: {len(task_queue)}")

    print("Задачи в очереди (через итератор):")
    for task in task_queue:
        print(f"  #{task.id}: {task.description[:40]}...")

    executor = AsyncTaskExecutor(task_queue=task_queue, num_workers=2)
    executor.register_handler(PrintHandler())

    async with executor:
        while len(task_queue) > 0:
            await asyncio.sleep(0.5)

    print("\nВсе задачи из очереди обработаны")


if __name__ == "__main__":
    asyncio.run(main())