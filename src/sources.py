class FileTaskSource:
    """описание класса"""

    def __init__(self, file_name: str):
        """

        :param file_name:
        """
        self.file_name = file_name

    def get_tasks(self) -> list[str]:
        """

        :return:
        """
        try:
            tasks = []
            with open(self.file_name, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    tasks.append(line)
            return tasks

        except FileNotFoundError:
            print(f"File {self.file_name} not found")
            return []


class GeneratorTaskSource:
    """описание класса"""
    def __init__(self, cnt: int):
        """
        описание функции
        :param cnt:
        """
        self._cnt = cnt

    @property
    def cnt(self):
        """
        описание функции
        :return:
        """
        return self._cnt

    @cnt.setter
    def cnt(self, value: int):
        """
        описание функции
        :param value:
        :return:
        """
        if value <= 0:
            raise ValueError("cnt must be greater than 0")
        self._cnt = value

    def get_tasks(self) -> list[str]:
        """
        описание функции
        :return:
        """
        tasks = []
        for i in range(1, self._cnt + 1):
            tasks.append(f"Task {i}")

        return tasks


class APITaskSource:
    """описание класса"""
    def get_tasks(self) -> list[str]:
        """
        описание функции
        :return:
        """
        return ["Сделать лабу", "Написать ридми", "Отправить Cамиру", "Доделать дизайн", "Начать писать фронт по практике"]
