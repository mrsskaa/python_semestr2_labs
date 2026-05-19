import asyncio
import pytest
from src.model import Task
from src.task_queue import TaskQueue
from src.async_executor import AsyncTaskExecutor
from src.handlers import PrintHandler


class SlowHandler:
    """Обработчик с задержкой для тестирования"""

    async def can_handle(self, task: Task) -> bool:
        return True

    async def handle(self, task: Task) -> None:
        await asyncio.sleep(0.1)

    async def cleanup(self) -> None:
        pass


@pytest.mark.asyncio
async def test_executor_processes_task():
    """Тест, что исполнитель обрабатывает задачу"""
    queue = TaskQueue()
    await queue.add(Task(id=1, description="Тестик", priority=3, status="pending"))

    executor = AsyncTaskExecutor(task_queue=queue, num_workers=1)
    executor.register_handler(PrintHandler())

    try:
        await executor.start()
        await asyncio.wait_for(asyncio.sleep(0.5), timeout=2.0)
        await executor.stop()
    finally:
        # Принудительная очистка
        for task in asyncio.all_tasks():
            if task is not asyncio.current_task():
                task.cancel()
        await asyncio.sleep(0.1)

    assert len(queue) == 0


@pytest.mark.asyncio
async def test_multiple_workers():
    """Тест, что несколько воркеров работают параллельно"""
    queue = TaskQueue()
    for i in range(1, 6):
        await queue.add(Task(id=i, description=f"Тест задача {i}", priority=3, status="pending"))

    executor = AsyncTaskExecutor(task_queue=queue, num_workers=3)
    executor.register_handler(SlowHandler())

    try:
        await executor.start()
        await asyncio.wait_for(asyncio.sleep(0.5), timeout=2.0)
        await executor.stop()
    finally:
        for task in asyncio.all_tasks():
            if task is not asyncio.current_task():
                task.cancel()
        await asyncio.sleep(0.1)

    assert len(queue) == 0


@pytest.mark.asyncio
async def test_handlers_registration():
    """Тест регистрации обработчиков"""
    queue = TaskQueue()
    executor = AsyncTaskExecutor(task_queue=queue, num_workers=1)

    assert len(executor.handlers) == 0

    executor.register_handler(PrintHandler())
    assert len(executor.handlers) == 1


@pytest.mark.asyncio
async def test_stop_executor():
    """Тест остановки исполнителя"""
    queue = TaskQueue()
    executor = AsyncTaskExecutor(task_queue=queue, num_workers=1)

    await executor.start()
    assert executor._stop is False

    await executor.stop()
    assert executor._stop is True
