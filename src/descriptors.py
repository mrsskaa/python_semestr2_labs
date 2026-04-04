import logging
from src.exceptions import TaskValidationError

logger = logging.getLogger(__name__)


class BaseDescriptor:
    """
    Базовый класс для data-дескрипторов с валидацией.

    Реализует общую логику __get__ и __set__, а метод validate
    переопределяется в наследниках.
    """

    def __set_name__(self, owner, name: str) -> None:
        """
        Сохраняет имя атрибута при создании класса.

        :param owner: класс, в котором создается дескриптор
        :param name: имя атрибута
        """
        self.name = name
        logger.debug(f"Дескриптор {self.__class__.__name__} привязан к атрибуту {name}")

    def __get__(self, instance, owner):
        """
        Возвращает значение атрибута.

        :param instance: экземпляр класса (None при доступе через класс)
        :param owner: класс экземпляра
        :return: значение атрибута или сам дескриптор
        """
        if instance is None:
            logger.debug(f"Доступ к дескриптору {self.name} через класс")
            return self
        value = instance.__dict__.get(self.name)
        logger.debug(f"Чтение атрибута {self.name}: {value}")
        return value

    def __set__(self, instance, value) -> None:
        """
        Устанавливает значение атрибута с валидацией.

        :param instance: экземпляр класса
        :param value: устанавливаемое значение
        :raises TaskValidationError: если значение не проходит валидацию
        """
        logger.debug(f"Попытка установить {self.name} = {value}")
        self.validate(self.name, value)
        instance.__dict__[self.name] = value
        logger.debug(f"Атрибут {self.name} установлен в {value}")

    def validate(self, name: str, value) -> None:
        """
        Проверяет значение атрибута. Переопределяется в наследниках.

        :param name: имя атрибута
        :param value: проверяемое значение
        :raises NotImplementedError: если не переопределен
        """
        raise NotImplementedError(f"Метод validate должен быть переопределен в {self.__class__.__name__}")


class PriorityDescriptor(BaseDescriptor):
    """Дескриптор для атрибута priority. Значение должно быть int от 1 до 5."""

    def validate(self, name: str, value: int) -> None:
        """
        Проверяет, что значение приоритета корректно.

        :param name: имя атрибута
        :param value: значение приоритета
        :raises TaskValidationError: если значение не int или вне диапазона 1-5
        """
        if not isinstance(value, int):
            logger.error(f"Попытка установить {name} = {value} (не int)")
            raise TaskValidationError(f"{name} должен быть целым числом")
        if value < 1 or value > 5:
            logger.error(f"Попытка установить {name} = {value} (вне диапазона 1-5)")
            raise TaskValidationError(f"{name} должен быть от 1 до 5")
        logger.debug(f"Валидация {name} = {value} пройдена")


class StatusDescriptor(BaseDescriptor):
    """Дескриптор для атрибута status. Значение должно быть одним из: pending, in_progress, completed."""

    def validate(self, name: str, value: str) -> None:
        """
        Проверяет, что значение статуса корректно.

        :param name: имя атрибута
        :param value: значение статуса
        :raises TaskValidationError: если значение не str или не в списке допустимых
        """
        if not isinstance(value, str):
            logger.error(f"Попытка установить {name} = {value} (не str)")
            raise TaskValidationError(f"{name} должен быть строкой")
        if value not in ["pending", "in_progress", "completed"]:
            logger.error(f"Попытка установить {name} = {value} (недопустимый статус)")
            raise TaskValidationError("Некорректный статус")
        logger.debug(f"Валидация {name} = {value} пройдена")


class DescriptionDescriptor(BaseDescriptor):
    """Дескриптор для атрибута description. Длина должна быть от 5 до 200 символов."""

    def validate(self, name: str, value: str) -> None:
        """
        Проверяет, что описание имеет допустимую длину.

        :param name: имя атрибута
        :param value: описание задачи
        :raises TaskValidationError: если значение не str или длина вне диапазона 5-200
        """
        if not isinstance(value, str):
            logger.error(f"Попытка установить {name} = {value} (не str)")
            raise TaskValidationError(f"{name} должен быть строкой")
        if len(value) < 5:
            logger.error(f"Попытка установить {name} длиной {len(value)} (мин 5)")
            raise TaskValidationError("Слишком короткое описание")
        if len(value) > 200:
            logger.error(f"Попытка установить {name} длиной {len(value)} (макс 200)")
            raise TaskValidationError("Слишком длинное описание")
        logger.debug(f"Валидация {name} (длина {len(value)}) пройдена")


class ReadyDescriptor:
    """
    Non-data дескриптор для вычисляемого свойства is_ready.

    Не имеет __set__, поэтому при присвоении значение сохраняется в __dict__,
    что демонстрирует разницу между data и non-data дескрипторами.
    """

    def __set_name__(self, owner, name: str) -> None:
        """
        Сохраняет имя атрибута при создании класса.

        :param owner: класс, в котором создается дескриптор
        :param name: имя атрибута
        """
        self.name = name
        logger.debug(f"Non-data дескриптор {self.__class__.__name__} привязан к {name}")

    def __get__(self, instance, owner):
        """
        Вычисляет готовность задачи к выполнению.

        Готовность = статус не "completed" И описание не пустое И длина описания >= 5.

        :param instance: экземпляр класса (None при доступе через класс)
        :param owner: класс экземпляра
        :return: True если задача готова к выполнению, иначе False
        """
        if instance is None:
            logger.debug(f"Доступ к non-data дескриптору {self.name} через класс")
            return self

        result = (instance.status != "completed" and
                  instance.description is not None and
                  len(instance.description) >= 5)

        logger.debug(f"Вычисление {self.name} = {result}")
        return result
