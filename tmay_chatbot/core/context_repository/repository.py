import logging
import os
from abc import ABC, abstractmethod

from langchain.embeddings import init_embeddings
from langchain_chroma import Chroma

from tmay_chatbot.core.models import Document, RetrievedDocument

logger = logging.getLogger(__name__)


class ContextRepository(ABC):
    @abstractmethod
    def store(self, documents: list[Document]) -> None: ...

    @abstractmethod
    def fetch(self, query: str, k: int = 10) -> list[RetrievedDocument]: ...

    @abstractmethod
    def fetch_all(self) -> list[RetrievedDocument]: ...


class ChromaContextRepository(ContextRepository):
    def __init__(self, db_path: str, embedding_model: str, collection_name: str):
        self.db_path = str(db_path)
        self.collection_name = collection_name
        self.embedding = init_embeddings(embedding_model)
        self._vectorstore: Chroma | None = None

    def _get_vectorstore(self) -> Chroma:
        if self._vectorstore is None:
            self._vectorstore = Chroma(
                persist_directory=self.db_path,
                embedding_function=self.embedding,
                collection_name=self.collection_name,
            )
        return self._vectorstore

    def store(self, documents: list[Document]) -> None:
        logger.info(f"Creating embeddings for {len(documents)} chunks")
        if os.path.exists(self.db_path):
            Chroma(
                persist_directory=self.db_path,
                embedding_function=self.embedding,
                collection_name=self.collection_name,
            ).delete_collection()

        self._vectorstore = Chroma.from_documents(
            documents=[document.to_langchain_document() for document in documents],
            embedding=self.embedding,
            persist_directory=self.db_path,
            collection_name=self.collection_name,
        )

        collection = self._vectorstore._collection
        count = collection.count()
        sample_embedding = collection.get(limit=1, include=["embeddings"])["embeddings"][0]
        dimensions = len(sample_embedding)
        logger.info(
            f"There are {count:,} vectors with {dimensions:,} dimensions in the vector store"
        )

    def fetch(self, query: str, k: int = 10) -> list[RetrievedDocument]:
        results = self._get_vectorstore().similarity_search_with_score(query, k=k)
        return [
            RetrievedDocument(content=lc_doc.page_content, metadata=lc_doc.metadata, score=score)
            for lc_doc, score in results
        ]

    def fetch_all(self) -> list[RetrievedDocument]:
        collection = self._get_vectorstore()._collection
        result = collection.get(include=["embeddings", "documents", "metadatas"])
        documents = [
            RetrievedDocument(content=content, metadata=metadata, embedding=list(embedding))
            for content, metadata, embedding in zip(
                result["documents"], result["metadatas"], result["embeddings"]
            )
        ]
        logger.info(f"Fetched {len(documents)} vectors from collection '{self.collection_name}'")
        return documents
