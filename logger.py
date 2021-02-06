import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def init_logger(log_path: Path):
    fmt = logging.Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")
    fh = RotatingFileHandler(log_path, maxBytes=10240, backupCount=10)
    fh.setFormatter(fmt)

    logger = logging.getLogger("bug_tracker")
    logger.addHandler(fh)
    logger.setLevel(logging.DEBUG)

