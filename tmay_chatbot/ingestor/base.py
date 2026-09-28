from abc import ABC, abstractmethod


class Ingestor(ABC):
    @abstractmethod
    def run(self):
        pass
