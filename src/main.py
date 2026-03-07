from src.sources import FileTaskSource, GeneratorTaskSource, APITaskSource
from src.processor import TaskProcessor

def main() -> None:
    """
    описание функции
    :return:
    """
    processor = TaskProcessor()

    file_source = FileTaskSource("tasks.txt")
    gen_source = GeneratorTaskSource(5)
    api_source = APITaskSource()

    processor.process(file_source)
    processor.process(gen_source)
    processor.process(api_source)

if __name__ == "__main__":
    main()
