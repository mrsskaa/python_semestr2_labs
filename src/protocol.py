from typing import Protocol, List, runtime_checkable

@runtime_checkable
class TaskSource(Protocol):
    def get_tasks(self) -> List[str]:
        ...
