from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_ROOT / ".env", override=True)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"), env_file_encoding="utf-8", extra="ignore"
    )

    # path to knowledge base, MD documents with relevant information
    knowledge_base_path: Path = PROJECT_ROOT / "knowledge-base"

    # vector database (Chroma)
    vector_db_path: Path = PROJECT_ROOT / "vector_db"
    collection_name: str = "tmay"

    # llm models
    chat_model: str = "gpt-5.1"
    embedding_model: str = "openai:text-embedding-3-large"
    eval_model: str = "gpt-4.1-nano"
    chunking_model: str = "gpt-4.1"

    # path to test.jsonl evaluation questions and answers
    tests_path: Path = PROJECT_ROOT / "tmay_chatbot" / "evaluation" / "tests.jsonl"

    # ingestor and chatbot version
    # v1 -> basic ingestor using K chunks, basic retrieval context before sending it to the LLM chat
    # v2 -> advance ingestor using an LLM to classify and order chunks, and also advance techniques to retrieve the
    # context before sending it to the LLM chat
    version: str = "v2"


settings = Settings()
