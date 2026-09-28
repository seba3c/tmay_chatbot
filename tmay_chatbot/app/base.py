import logging
from abc import ABC, abstractmethod

from tmay_chatbot.utils.logging_config import configure_logging

logger = logging.getLogger(__name__)


class App(ABC):
    def run(self, *args, **kwargs) -> None:
        configure_logging()
        logger.info(f"Running {self.name}...")
        self.run_hook(*args, **kwargs)
        logger.info("Bye!")

    @abstractmethod
    def run_hook(self, *args, **kwargs) -> None:
        pass

    @property
    def name(self) -> str:
        return type(self).__name__


class CliApp(App):
    pass


class GradioApp(App):
    pass


class PlotlyApp(App):
    pass
