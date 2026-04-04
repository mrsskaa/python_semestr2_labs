import pytest
from src.sources import FileTaskSource
from src.model import Task


@pytest.fixture
def temp_task_file(tmp_path):
    """Создает временный файл с задачами для тестирования"""
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


def test_file_source_reads_tasks(temp_task_file):
    """Тест чтения задач из существующего файла"""
    source = FileTaskSource(temp_task_file)
    tasks = source.get_tasks()

    assert len(tasks) == 4
    assert all(isinstance(t, Task) for t in tasks)
    assert tasks[0].description == "Задача 1"
    assert tasks[1].description == "Задача 2"
    assert tasks[2].description == "Задача 3"
    assert tasks[3].description == "Задача 4"


def test_file_source_skips_empty_lines(temp_task_file):
    """Тест игнорирования пустых строк"""
    source = FileTaskSource(temp_task_file)
    tasks = source.get_tasks()

    for task in tasks:
        assert task.description != ""
        assert not task.description.isspace()


def test_file_source_file_not_found():
    """Тест обработки отсутствующего файла"""
    source = FileTaskSource("non_existent_file.txt")
    tasks = source.get_tasks()

    assert tasks == []


def test_file_source_empty_file(empty_file):
    """Тест чтения пустого файла"""
    source = FileTaskSource(empty_file)
    tasks = source.get_tasks()

    assert tasks == []


def test_file_source_returns_list_of_strings(temp_task_file):
    """Тест возвращаемого типа"""
    source = FileTaskSource(temp_task_file)
    tasks = source.get_tasks()

    assert isinstance(tasks, list)
    assert all(isinstance(task, Task) for task in tasks)
