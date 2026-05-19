import asyncio
import pytest
from src.sources import FileTaskSource, GeneratorTaskSource, APITaskSource, HTTPClient
from src.task_queue import TaskQueue
from src.model import Task


@pytest.fixture
def file_source(temp_task_file):
    """Фикстура для FileTaskSource"""
    return FileTaskSource(temp_task_file)


@pytest.fixture
def generator_source():
    """Фикстура для GeneratorTaskSource"""
    return GeneratorTaskSource(5)


@pytest.fixture
def api_source():
    """Фикстура для APITaskSource с HTTPClient"""
    client = HTTPClient()
    return APITaskSource(http_client=client)


@pytest.fixture
def temp_task_file(tmp_path):
    """Создает временный файл с задачами"""
    file_path = tmp_path / "tasks.txt"
    content = "Задача 1\nЗадача 2\n\nЗадача 3\n  \nЗадача 4"
    file_path.write_text(content, encoding='utf-8')
    return str(file_path)


@pytest.fixture
def empty_file(tmp_path):
    """Создает пустой файл"""
    file_path = tmp_path / "empty.txt"
    file_path.write_text("", encoding='utf-8')
    return str(file_path)


@pytest.fixture
def task_queue():
    """Фикстура для пустой очереди задач"""
    return TaskQueue()


@pytest.fixture
def filled_task_queue():
    """Фикстура для очереди с тремя задачами"""
    queue = TaskQueue()
    queue._tasks = [
        Task(id=1, description="Задача 1", priority=1, status="pending"),
        Task(id=2, description="Задача 2", priority=3, status="in_progress"),
        Task(id=3, description="Задача 3", priority=5, status="completed"),
    ]
    return queue
