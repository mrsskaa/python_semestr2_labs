import pytest
from src.sources import FileTaskSource
from src.model import Task


@pytest.mark.asyncio
async def test_file_source_reads_tasks(temp_task_file):
    """Тест чтения задач из существующего файла"""
    source = FileTaskSource(temp_task_file)
    tasks = await source.get_tasks()

    assert len(tasks) == 4
    assert all(isinstance(t, Task) for t in tasks)
    assert tasks[0].description == "Задача 1"
    assert tasks[1].description == "Задача 2"
    assert tasks[2].description == "Задача 3"
    assert tasks[3].description == "Задача 4"


@pytest.mark.asyncio
async def test_file_source_skips_empty_lines(temp_task_file):
    """Тест игнорирования пустых строк"""
    source = FileTaskSource(temp_task_file)
    tasks = await source.get_tasks()

    for task in tasks:
        assert task.description != ""
        assert not task.description.isspace()


@pytest.mark.asyncio
async def test_file_source_file_not_found():
    """Тест обработки отсутствующего файла"""
    source = FileTaskSource("non_existent_file.txt")
    tasks = await source.get_tasks()

    assert tasks == []


@pytest.mark.asyncio
async def test_file_source_empty_file(empty_file):
    """Тест чтения пустого файла"""
    source = FileTaskSource(empty_file)
    tasks = await source.get_tasks()

    assert tasks == []


@pytest.mark.asyncio
async def test_file_source_returns_list_of_tasks(temp_task_file):
    """Тест возвращаемого типа"""
    source = FileTaskSource(temp_task_file)
    tasks = await source.get_tasks()

    assert isinstance(tasks, list)
    assert all(isinstance(task, Task) for task in tasks)


@pytest.mark.asyncio
async def test_file_source_supports_async_iteration(temp_task_file):
    """Источник поддерживает async for (итераторы/генераторы на источнике)."""
    source = FileTaskSource(temp_task_file)
    tasks = [task async for task in source]
    assert [t.description for t in tasks] == ["Задача 1", "Задача 2", "Задача 3", "Задача 4"]
