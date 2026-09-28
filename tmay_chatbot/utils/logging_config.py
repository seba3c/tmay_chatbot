import logging


def configure_logging(level: int = logging.INFO) -> None:
    """Configure the root logger with a standard format.

    Args:
        level: Minimum severity to log. Defaults to logging.INFO.
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
