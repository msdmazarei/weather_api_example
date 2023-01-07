from typing import TypeAlias

import loguru
from loguru import logger as logger_instance

Logger: TypeAlias = "loguru._logger.Logger"


def get_logger() -> Logger:
    return logger_instance


__all__ = ["get_logger", "Logger"]
