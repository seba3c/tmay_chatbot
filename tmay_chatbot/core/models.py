from langchain_core.documents import Document as LCDocument
from pydantic import BaseModel


class Document(BaseModel):
    content: str
    metadata: dict

    def to_langchain_document(self) -> LCDocument:
        return LCDocument(page_content=self.content, metadata=self.metadata)


class RetrievedDocument(Document):
    score: float | None = None
    embedding: list[float] | None = None
