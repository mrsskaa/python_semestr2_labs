import pytest
from src.sources import APITaskSource, HTTPClient
from src.model import Task


@pytest.mark.asyncio
async def test_api_source_returns_list():
    """Тест возвращаемого типа"""
    client = HTTPClient()
    source = APITaskSource(http_client=client)
    tasks = await source.get_tasks()

    assert isinstance(tasks, list)


@pytest.mark.asyncio
async def test_api_source_returns_tasks():
    """Тест, что все элементы списка - Task"""
    client = HTTPClient()
    source = APITaskSource(http_client=client)
    tasks = await source.get_tasks()

    assert all(isinstance(task, Task) for task in tasks)


@pytest.mark.asyncio
async def test_api_source_has_correct_data():
    """Тест, что данные из API корректно преобразуются"""
    client = HTTPClient()
    source = APITaskSource(http_client=client)
    tasks = await source.get_tasks()

    assert len(tasks) == 2
    assert tasks[0].id == 1
    assert tasks[0].description == "Задача из API 1"
    assert tasks[1].id == 2
    assert tasks[1].description == "Задача из API 2"


@pytest.mark.asyncio
async def test_api_source_custom_url():
    """Тест с кастомным URL"""
    client = HTTPClient()
    source = APITaskSource(http_client=client, api_url="https://custom.api.com/tasks")
    tasks = await source.get_tasks()

    assert isinstance(tasks, list)
    assert len(tasks) == 2
