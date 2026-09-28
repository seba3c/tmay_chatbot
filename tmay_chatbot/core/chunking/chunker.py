from abc import ABC, abstractmethod

from tmay_chatbot.core.models import Document


class Chunker(ABC):
    @abstractmethod
    def get_chunks(self, documents: list[Document]) -> list[Document]: ...
