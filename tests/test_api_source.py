import pytest
from src.sources import APITaskSource
from src.model import Task

def test_api_source_returns_fixed_list():
    """Тест возврата фиксированного списка задач"""
    source = APITaskSource()
    tasks = source.get_tasks()

    # Ожидаемые описания задач
    expected_descriptions = [
        "Сделать лабу",
        "Написать ридми",
        "Отправить Cамиру",
        "Доделать дизайн",
        "Начать писать фронт по практике"
    ]

    assert len(tasks) == 5
    for i, task in enumerate(tasks):
        assert task.description == expected_descriptions[i]
        assert task.id == i + 1
        assert task.priority == 3
        assert task.status == "pending"


def test_api_source_returns_list():
    """Тест возвращаемого типа"""
    source = APITaskSource()
    tasks = source.get_tasks()

    assert isinstance(tasks, list)


def test_api_source_returns_task_objects():
    """Тест, что все элементы списка - объекты Task"""
    source = APITaskSource()
    tasks = source.get_tasks()

    assert all(isinstance(task, Task) for task in tasks)


def test_api_source_consistent_return():
    """Тест, что при повторных вызовах возвращаются одинаковые данные (но разные объекты)"""
    source = APITaskSource()
    tasks1 = source.get_tasks()
    tasks2 = source.get_tasks()

    assert len(tasks1) == len(tasks2)
    for t1, t2 in zip(tasks1, tasks2):
        assert t1.id == t2.id
        assert t1.description == t2.description
        assert t1.priority == t2.priority
        assert t1.status == t2.status

    assert tasks1 is not tasks2
    assert all(t1 is not t2 for t1, t2 in zip(tasks1, tasks2))


def test_api_source_task_attributes():
    """Тест атрибутов каждого Task объекта"""
    source = APITaskSource()
    tasks = source.get_tasks()

    for task in tasks:
        assert hasattr(task, 'id')
        assert hasattr(task, 'description')
        assert hasattr(task, 'priority')
        assert hasattr(task, 'status')
        assert isinstance(task.id, int)
        assert isinstance(task.description, str)
        assert isinstance(task.priority, int)
        assert isinstance(task.status, str)