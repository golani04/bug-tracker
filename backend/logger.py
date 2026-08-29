import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Union


logger = logging.getLogger("bug_tracker")


def init_logger(_log_path: Path | None = None) -> None:
    log_path: Union[str, Path] = _log_path or Path().joinpath("logs", "bug_tracker.log").resolve()

    formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")
    file_handler = RotatingFileHandler(log_path, maxBytes=10240, backupCount=10)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # set handlers for the current logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG)
