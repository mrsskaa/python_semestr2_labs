import pytest
from src.sources import GeneratorTaskSource
from src.model import Task


def test_generator_creates_correct_number_of_tasks():
    """Тест генерации правильного количества задач"""
    source = GeneratorTaskSource(5)
    tasks = source.get_tasks()

    assert len(tasks) == 5


def test_generator_task_format():
    """Тест формата генерируемых задач"""
    source = GeneratorTaskSource(3)
    tasks = source.get_tasks()

    assert tasks[0].id == 1 and tasks[0].description.startswith("Сгенерированная задача")
    assert tasks[1].id == 2
    assert tasks[2].id == 3


def test_generator_cnt_property_initial_value():
    """Тест начального значения свойства cnt"""
    source = GeneratorTaskSource(10)
    assert source.cnt == 10


def test_generator_cnt_setter_valid_value():
    """Тест установки корректного значения через сеттер"""
    source = GeneratorTaskSource(5)
    source.cnt = 15

    assert source.cnt == 15
    tasks = source.get_tasks()
    assert len(tasks) == 15


def test_generator_cnt_setter_invalid_value():
    """Тест установки некорректного значения через сеттер"""
    source = GeneratorTaskSource(5)

    with pytest.raises(ValueError, match="cnt must be greater than 0"):
        source.cnt = 0

    with pytest.raises(ValueError, match="cnt must be greater than 0"):
        source.cnt = -3


def test_generator_zero_tasks_in_init():
    """Тест инициализации с нулевым количеством задач"""
    with pytest.raises(ValueError, match="cnt must be greater than 0"):
        GeneratorTaskSource(0)


def test_generator_negative_tasks_in_init():
    """Тест инициализации с отрицательным количеством задач"""
    with pytest.raises(ValueError, match="cnt must be greater than 0"):
        GeneratorTaskSource(-5)


def test_generator_returns_list_of_tasks():
    """Тест возвращаемого типа"""
    source = GeneratorTaskSource(3)
    tasks = source.get_tasks()

    assert isinstance(tasks, list)
    assert all(isinstance(task, Task) for task in tasks)
