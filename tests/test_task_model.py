import datetime
import pytest

from src.descriptors import (
    BaseDescriptor,
    DescriptionDescriptor,
    PriorityDescriptor,
    ReadyDescriptor,
    StatusDescriptor,
)
from src.exceptions import TaskError, TaskValidationError
from src.model import Task


def _valid_kwargs() -> dict:
    return {
        "id": 1,
        "description": "Достаточно длинное описание задачи",
        "priority": 3,
        "status": "pending",
    }


def test_task_creation_and_readonly_properties():
    """Создание задачи: id и created_at доступны, created_at задаётся при создании."""
    before = datetime.datetime.now()
    task = Task(**_valid_kwargs())
    after = datetime.datetime.now()

    assert task.id == 1
    assert isinstance(task.created_at, datetime.datetime)
    assert before <= task.created_at <= after


def test_id_cannot_be_changed_after_init():
    """Повторная установка id запрещена (property + инвариант)."""
    task = Task(**_valid_kwargs())

    with pytest.raises(AttributeError, match="id нельзя изменить"):
        task.id = 2


def test_id_must_be_positive():
    """Некорректный id при создании — TaskValidationError."""
    kw = _valid_kwargs()
    kw["id"] = 0

    with pytest.raises(TaskValidationError, match="id должен быть больше 0"):
        Task(**kw)


def test_priority_validation_type_and_range():
    """PriorityDescriptor: тип int и диапазон 1–5."""
    task = Task(**_valid_kwargs())

    with pytest.raises(TaskValidationError, match="целым числом"):
        task.priority = "3"

    with pytest.raises(TaskValidationError, match="от 1 до 5"):
        task.priority = 0

    with pytest.raises(TaskValidationError, match="от 1 до 5"):
        task.priority = 6

    task.priority = 1
    assert task.priority == 1


def test_status_validation():
    """StatusDescriptor: только допустимые строковые статусы."""
    task = Task(**_valid_kwargs())

    with pytest.raises(TaskValidationError, match="строкой"):
        task.status = 1

    with pytest.raises(TaskValidationError, match="Некорректный статус"):
        task.status = "unknown"

    task.status = "in_progress"
    assert task.status == "in_progress"


def test_description_validation_length():
    """DescriptionDescriptor: длина 5–200 символов."""
    task = Task(**_valid_kwargs())

    with pytest.raises(TaskValidationError, match="строкой"):
        task.description = None  # type: ignore[assignment]

    with pytest.raises(TaskValidationError, match="короткое"):
        task.description = "корт"

    with pytest.raises(TaskValidationError, match="длинное"):
        task.description = "x" * 201

    task.description = "Нормальное описание задачи"
    assert len(task.description) >= 5


def test_is_ready_computed_for_non_data_descriptor():
    """Non-data дескриптор is_ready: True для незавершённой задачи с валидным описанием."""
    task = Task(**_valid_kwargs())
    assert task.is_ready is True

    task.status = "completed"
    assert task.is_ready is False


def test_non_data_descriptor_assignment_shadows_computed_property():
    """При присваивании is_ready значение попадает в __dict__ (отличие от data-дескриптора)."""
    task = Task(**_valid_kwargs())
    assert task.is_ready is True

    task.is_ready = False
    assert task.__dict__.get("is_ready") is False
    assert task.is_ready is False


def test_data_descriptors_access_via_class():
    """Доступ к data-дескрипторам через класс возвращает объект дескриптора."""
    assert isinstance(Task.priority, PriorityDescriptor)
    assert isinstance(Task.status, StatusDescriptor)
    assert isinstance(Task.description, DescriptionDescriptor)
    assert isinstance(Task.is_ready, ReadyDescriptor)


def test_base_descriptor_not_implemented_validate():
    """BaseDescriptor без переопределения validate вызывает NotImplementedError при записи."""

    class Broken(BaseDescriptor):
        pass

    class Holder:
        x = Broken()

    with pytest.raises(NotImplementedError):
        Holder().x = 1


def test_task_validation_error_is_task_error():
    """Иерархия исключений домена задач."""
    assert issubclass(TaskValidationError, TaskError)
    err = TaskValidationError("msg")
    assert isinstance(err, TaskError)


def test_init_validates_all_fields():
    """Некорректные данные в конструкторе отклоняются до полной инициализации (priority)."""
    kw = _valid_kwargs()
    kw["priority"] = 10

    with pytest.raises(TaskValidationError):
        Task(**kw)
