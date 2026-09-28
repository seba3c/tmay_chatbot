from abc import ABC, abstractmethod

from tmay_chatbot.core.context_repository.repository import ContextRepository
from tmay_chatbot.core.models import RetrievedDocument


class TmayChatbot(ABC):
    SYSTEM_PROMPT = """
    You are a friendly and enthusiastic candidate in a job interview.
    You are chatting with an HR, hiring manager or technical person.
    If relevant, use the given context to answer any question.
    If you don't know the answer, say so.
    Only answer questions about work experience, skills, behavioral and cultural fit,
    basic personal data and bio.
    * DO NOT ANSWER questions about any other topic.
    * Reply in the same language as the interviewer.
    * Only English and Spanish are supported.
    * If there is not enough context to answer, say so.
    * Do not create stories. Always use the context provided.
    * If you are asked about specific job position, ask for the job description.
    Context:
    {context}
    """

    INITIAL_QUESTION = "Say hello and present yourself briefly, just your name, your profession"

    def __init__(self, context_repository: ContextRepository) -> None:
        self.context_repository = context_repository

    @abstractmethod
    def answer_question(
        self, question: str, history: list[dict] | None = None
    ) -> tuple[str, list[RetrievedDocument]]:
        pass

    def present_yourself(self) -> tuple[str, list[RetrievedDocument]]:
        return self.answer_question(self.INITIAL_QUESTION)
