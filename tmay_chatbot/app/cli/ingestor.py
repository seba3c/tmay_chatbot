import logging

from tmay_chatbot.app.base import CliApp
from tmay_chatbot.ingestor.factory import get_ingestor

logger = logging.getLogger(__name__)


class IngestorApp(CliApp):
    def run_hook(self, *args, **kwargs) -> None:
        get_ingestor().run()


if __name__ == "__main__":
    IngestorApp().run()
