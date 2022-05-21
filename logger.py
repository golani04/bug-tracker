import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Union


def init_logger(_log_path: Path | None = None) -> None:
    log_path: Union[str, Path] = _log_path or Path().joinpath("logs", "bug_tracker.log").resolve()

    fmt = logging.Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")
    fh = RotatingFileHandler(log_path, maxBytes=10240, backupCount=10)
    fh.setFormatter(fmt)

    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(fmt)

    logger = logging.getLogger("bug_tracker")
    # set handlers for the current logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.setLevel(logging.DEBUG)
