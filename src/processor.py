from src.protocol import TaskSource

class TaskProcessor():
    def process(self, source: TaskSource) -> list[str]:
        if not isinstance(source, TaskSource):
            raise TypeError(f"The object {source} isn't the source of the tasks")

        tasks = source.get_tasks()
        print(f"Tasks cnt: {len(tasks)} tasks:  {tasks}")
        return tasks
