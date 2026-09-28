import glob
import logging
import os
from abc import ABC, abstractmethod
from pathlib import Path

from tmay_chatbot.core.models import Document

logger = logging.getLogger(__name__)


class KnowledgeBaseRepository(ABC):
    @abstractmethod
    def fetch_documents(self) -> list[Document]: ...

    @abstractmethod
    def fetch_doc_types(self) -> list[str]: ...


class MarkdownKnowledgeBaseRepository(KnowledgeBaseRepository):
    def __init__(self, dir_path: str):
        self.dir_path = dir_path

    def fetch_documents(self) -> list[Document]:
        folders = glob.glob(f"{self.dir_path}/*")
        logger.info(f"Loading documents from: {folders}...")
        documents = []
        for folder in folders:
            doc_type = os.path.basename(folder)
            for file_path in Path(folder).glob("**/*.md"):
                text = file_path.read_text(encoding="utf-8")
                documents.append(
                    Document(
                        content=text,
                        metadata={"source": str(file_path), "doc_type": doc_type},
                    )
                )
        logger.info(f"{len(documents)} documents loaded!")
        return documents

    def fetch_doc_types(self) -> list[str]:
        folders = glob.glob(f"{self.dir_path}/*")
        return sorted(os.path.basename(folder) for folder in folders if os.path.isdir(folder))
