import pytest
from src.protocol import TaskSource
from src.processor import TaskProcessor
from src.sources import FileTaskSource, GeneratorTaskSource, APITaskSource
from src.model import Task


class MockSource:
    """Мок-класс для тестирования"""
    def __init__(self, tasks=None):
        self._tasks = tasks or ["mock1", "mock2"]
        self.get_tasks_called = False

    def get_tasks(self):
        self.get_tasks_called = True
        return self._tasks


class NonCompliantSource:
    """Класс, не соответствующий протоколу (нет метода get_tasks)."""
    pass


def test_processor_accepts_valid_source():
    """Тест, что процессор принимает корректный источник."""
    processor = TaskProcessor()
    source = MockSource()

    result = processor.process(source)

    assert source.get_tasks_called
    assert result == ["mock1", "mock2"]


def test_processor_returns_tasks():
    """Тест, что процессор возвращает задачи."""
    processor = TaskProcessor()
    source = MockSource(["task1", "task2"])

    result = processor.process(source)

    assert result == ["task1", "task2"]
    assert isinstance(result, list)


def test_processor_rejects_non_compliant_source():
    """Тест, что процессор отвергает источник без get_tasks"""
    processor = TaskProcessor()
    source = NonCompliantSource()

    with pytest.raises(TypeError) as excinfo:
        processor.process(source)

    assert "isn't the source of the tasks" in str(excinfo.value)


def test_processor_works_with_file_source(temp_task_file):
    """Тест, что процессор работает с FileTaskSource"""
    processor = TaskProcessor()
    source = FileTaskSource(temp_task_file)

    result = processor.process(source)

    assert isinstance(result, list)
    assert len(result) > 0


def test_processor_works_with_generator_source():
    """Тест, что процессор работает с GeneratorTaskSource"""
    processor = TaskProcessor()
    source = GeneratorTaskSource(3)

    result = processor.process(source)

    assert len(result) == 3
    assert all(isinstance(t, Task) for t in result)
    assert [t.id for t in result] == [1, 2, 3]


def test_processor_works_with_api_source():
    """Тест, что процессор работает с APITaskSource"""
    processor = TaskProcessor()
    source = APITaskSource()

    result = processor.process(source)

    expected = [
        "Сделать лабу",
        "Написать ридми",
        "Отправить Cамиру",
        "Доделать дизайн",
        "Начать писать фронт по практике"
    ]
    assert [t.description for t in result] == expected


def test_processor_isinstance_check_uses_protocol():
    """Тест, что проверка isinstance использует протокол"""
    processor = TaskProcessor()
    source = MockSource()

    assert isinstance(source, TaskSource)

    result = processor.process(source)
    assert result == ["mock1", "mock2"]


@pytest.fixture
def temp_task_file(tmp_path):
    """Создает временный файл с задачами для тестирования"""
    file_path = tmp_path / "tasks.txt"
    content = "Задача 1\nЗадача 2\nЗадача 3"
    file_path.write_text(content, encoding='utf-8')
    return str(file_path)
