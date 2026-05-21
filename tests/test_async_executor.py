import asyncio

import pytest

from src.async_executor import AsyncTaskExecutor
from src.handlers import PrintHandler
from src.model import Task
from src.task_queue import TaskQueue


class SlowHandler:
    """Обработчик с задержкой для тестирования параллельной обработки."""

    async def can_handle(self, task: Task) -> bool:
        return True

    async def handle(self, task: Task) -> None:
        await asyncio.sleep(0.05)

    async def cleanup(self) -> None:
        pass


async def _wait_until_queue_empty(queue: TaskQueue, timeout: float = 3.0) -> None:
    """Ждёт, пока очередь опустеет, или падает по таймауту."""
    deadline = asyncio.get_running_loop().time() + timeout
    while len(queue) > 0:
        if asyncio.get_running_loop().time() > deadline:
            raise TimeoutError("Очередь не опустела за отведённое время")
        await asyncio.sleep(0.05)


@pytest.mark.asyncio
async def test_executor_processes_task():
    """Исполнитель обрабатывает задачу и опустошает очередь."""
    queue = TaskQueue()
    await queue.add(Task(id=1, description="Тестик", priority=3, status="pending"))

    executor = AsyncTaskExecutor(task_queue=queue, num_workers=1)
    executor.register_handler(SlowHandler())

    async with executor:
        await _wait_until_queue_empty(queue)

    assert len(queue) == 0


@pytest.mark.asyncio
async def test_multiple_workers():
    """Несколько воркеров параллельно обрабатывают пакет задач."""
    queue = TaskQueue()
    for i in range(1, 6):
        await queue.add(Task(id=i, description=f"Тест задача {i}", priority=3, status="pending"))

    executor = AsyncTaskExecutor(task_queue=queue, num_workers=3)
    executor.register_handler(SlowHandler())

    async with executor:
        await _wait_until_queue_empty(queue)

    assert len(queue) == 0


@pytest.mark.asyncio
async def test_handlers_registration():
    """Регистрация обработчиков в исполнителе."""
    queue = TaskQueue()
    executor = AsyncTaskExecutor(task_queue=queue, num_workers=1)

    assert len(executor.handlers) == 0

    executor.register_handler(PrintHandler())
    assert len(executor.handlers) == 1


@pytest.mark.asyncio
async def test_stop_executor():
    """Остановка исполнителя завершает воркеров без зависания."""
    queue = TaskQueue()
    executor = AsyncTaskExecutor(task_queue=queue, num_workers=1)

    await executor.start()
    assert executor._stop is False

    await executor.stop()
    assert executor._stop is True
    assert all(worker.done() for worker in executor.workers)
