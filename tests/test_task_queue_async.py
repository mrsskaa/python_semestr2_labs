import asyncio
import pytest
from src.model import Task
from src.task_queue import TaskQueue


@pytest.mark.asyncio
async def test_async_add():
    """Тест асинхронного добавления задачи"""
    queue = TaskQueue()
    await queue.add(Task(id=1, description="Тест задача", priority=3, status="pending"))

    assert len(queue) == 1


@pytest.mark.asyncio
async def test_async_pop():
    """Тест асинхронного извлечения задачи"""
    queue = TaskQueue()
    await queue.add(Task(id=1, description="Тест задача", priority=3, status="pending"))

    task = await queue.pop()

    assert task.id == 1
    assert len(queue) == 0


@pytest.mark.asyncio
async def test_pop_waits_for_task():
    """Тест, что pop ждет появления задачи"""
    queue = TaskQueue()

    async def add_later():
        await asyncio.sleep(0.2)
        await queue.add(Task(id=1, description="Тест задача", priority=3, status="pending"))

    asyncio.create_task(add_later())
    task = await queue.pop()

    assert task.id == 1


@pytest.mark.asyncio
async def test_pop_returns_correct_order():
    """Тест, что задачи извлекаются в правильном порядке (FIFO)"""
    queue = TaskQueue()
    await queue.add(Task(id=1, description="Первая задача", priority=3, status="pending"))
    await queue.add(Task(id=2, description="Вторая задача", priority=3, status="pending"))
    await queue.add(Task(id=3, description="Третья задача", priority=3, status="pending"))

    task1 = await queue.pop()
    task2 = await queue.pop()
    task3 = await queue.pop()

    assert task1.id == 1
    assert task2.id == 2
    assert task3.id == 3


@pytest.mark.asyncio
async def test_pop_returns_none_when_closed():
    """pop на закрытой пустой очереди возвращает None."""
    queue = TaskQueue()
    queue.close()
    assert await queue.pop() is None


@pytest.mark.asyncio
async def test_pop_on_empty_then_add():
    """Тест: pop на пустой очереди, потом добавление"""
    queue = TaskQueue()

    async def add_task():
        await asyncio.sleep(0.2)
        await queue.add(Task(id=1, description="Тест задача", priority=3, status="pending"))

    asyncio.create_task(add_task())
    task = await queue.pop()

    assert task is not None
    assert task.id == 1
