import pytest
from src.sources import APITaskSource


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

    assert tasks == expected
    assert len(tasks) == 5


def test_api_source_returns_list():
    """Тест возвращаемого типа"""
    source = APITaskSource()
    tasks = source.get_tasks()

    assert isinstance(tasks, list)


def test_api_source_returns_strings():
    """Тест, что все элементы списка - строки"""
    source = APITaskSource()
    tasks = source.get_tasks()

    assert all(isinstance(task, str) for task in tasks)


def test_api_source_consistent_return():
    """Тест, что при повторных вызовах возвращается тот же список"""
    source = APITaskSource()
    tasks1 = source.get_tasks()
    tasks2 = source.get_tasks()

    assert tasks1 == tasks2
    assert tasks1 is not tasks2
