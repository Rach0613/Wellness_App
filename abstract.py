from abc import ABC, abstractmethod


class AbstractScreen(ABC):
    @abstractmethod
    def on_enter(self):
        pass


class AbstractFileOperation(ABC):
    @abstractmethod
    def perform_file_operation(self, filename, mode="r", data=None):
        pass
