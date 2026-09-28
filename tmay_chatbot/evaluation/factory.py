from tmay_chatbot.chatbot.factory import get_chatbot
from tmay_chatbot.evaluation.eval import ChatbotEvaluator
from tmay_chatbot.settings import settings


def get_chatbot_evaluator() -> ChatbotEvaluator:
    return ChatbotEvaluator(
        chatbot=get_chatbot(),
        eval_model=settings.eval_model,
        tests_path=settings.tests_path,
    )
