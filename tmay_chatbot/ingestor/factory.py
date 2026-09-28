from tmay_chatbot.ingestor.v2 import AdvancedIngestor
from tmay_chatbot.ingestor.v1 import BasicIngestor
from tmay_chatbot.settings import settings


def get_ingestor():
    if settings.version == "v1":
        return BasicIngestor()
    elif settings.version == "v2":
        return AdvancedIngestor()
    raise RuntimeError(f"Unknown version: {settings.version}")
