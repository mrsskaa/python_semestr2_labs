import pytest
from src.sources import APITaskSource
from src.model import Task


def test_api_source_returns_fixed_list():
    """Тест возврата фиксированного списка задач"""
    source = APITaskSource()
    tasks = source.get_tasks()

    expected = [
        "Сделать лабу",
        "Написать ридми",
        "Отправить Cамиру",
        "Доделать дизайн",
        "Начать писать фронт по практике"
    ]

    assert [task.description for task in tasks] == expected
    assert len(tasks) == 5


def test_api_source_returns_list():
    """Тест возвращаемого типа"""
    source = APITaskSource()
    tasks = source.get_tasks()

    assert isinstance(tasks, list)


def test_api_source_returns_tasks():
    """Тест, что все элементы списка - Task"""
    source = APITaskSource()
    tasks = source.get_tasks()

    assert all(isinstance(task, Task) for task in tasks)


def test_api_source_consistent_return():
    """Тест, что при повторных вызовах возвращается тот же список"""
    source = APITaskSource()
    tasks1 = source.get_tasks()
    tasks2 = source.get_tasks()

    assert [t.description for t in tasks1] == [t.description for t in tasks2]
    assert tasks1 is not tasks2
