import pytest
import asyncio
from src.model import Task
from src.task_queue import TaskQueue


def make_task(task_id: int, description: str, priority: int, status: str) -> Task:
    """Создаёт объект Task для тестовых сценариев"""
    return Task(
        id=task_id,
        description=description,
        priority=priority,
        status=status,
    )


def test_queue_iterates_all_tasks() -> None:
    """Тест, что очередь корректно итерируется по всем задачам"""
    tasks = [
        make_task(1, "Сделать отчет", 2, "pending"),
        make_task(2, "Проверить PR", 4, "in_progress"),
    ]
    queue = TaskQueue(tasks)
    assert [task.id for task in queue] == [1, 2]


def test_queue_can_be_iterated_twice() -> None:
    """Тест, что очередь поддерживает повторный обход"""
    queue = TaskQueue([make_task(1, "Первая задача", 3, "pending")])
    first_pass = [task.id for task in queue]
    second_pass = [task.id for task in queue]
    assert first_pass == [1]
    assert second_pass == [1]


@pytest.mark.asyncio
async def test_queue_add_and_len() -> None:
    """Тест добавления задачи и подсчёта длины очереди"""
    queue = TaskQueue()
    await queue.add(make_task(1, "Новая задача", 5, "pending"))
    assert len(queue) == 1


def test_filter_by_status_is_lazy_and_correct() -> None:
    """Тест ленивой фильтрации задач по статусу"""
    queue = TaskQueue(
        [
            make_task(1, "Task A", 1, "pending"),
            make_task(2, "Task B", 3, "completed"),
            make_task(3, "Task C", 2, "pending"),
        ]
    )
    result = queue.iter_by_status("pending")
    assert not isinstance(result, list)
    assert [task.id for task in result] == [1, 3]


def test_filter_by_priority_is_lazy_and_correct() -> None:
    """Тест ленивой фильтрации задач по диапазону приоритета"""
    queue = TaskQueue(
        [
            make_task(1, "Task A", 1, "pending"),
            make_task(2, "Task B", 3, "in_progress"),
            make_task(3, "Task C", 5, "completed"),
        ]
    )
    result = queue.iter_by_priority(min_priority=2, max_priority=4)
    assert not isinstance(result, list)
    assert [task.id for task in result] == [2]


def test_queue_compatible_with_list_and_sum() -> None:
    """Тест совместимости очереди с list() и sum()"""
    queue = TaskQueue(
        [
            make_task(1, "Task A", 2, "pending"),
            make_task(2, "Task B", 4, "completed"),
        ]
    )
    as_list = list(queue)
    total_priority = sum(task.priority for task in queue)
    assert len(as_list) == 2
    assert total_priority == 6


def test_empty_queue_iteration() -> None:
    """Тест корректной итерации и фильтрации пустой очереди"""
    queue = TaskQueue()
    assert list(queue) == []
    assert list(queue.iter_by_status("pending")) == []
    assert list(queue.iter_by_priority(min_priority=1)) == []


def test_empty_iterator_raises_stop_iteration() -> None:
    """Тест корректной обработки StopIteration на пустой очереди."""
    queue = TaskQueue()
    iterator = iter(queue)

    with pytest.raises(StopIteration):
        next(iterator)
