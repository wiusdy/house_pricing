import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = "logs"
LOG_FILE = "house_pricing.log"
MAX_LOG_SIZE = 5_000_000  # 5MB
BACKUP_COUNT = 3

# Ensure the logs directory exists
os.makedirs(LOG_DIR, exist_ok=True)

def configure_logger(name: str) -> logging.Logger:
    """
    Create and configure a logger with the given name.
    Returns an existing logger if already created.
    """
    logger = logging.getLogger(name)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # File handler with rotation
    file_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, LOG_FILE),
        maxBytes=MAX_LOG_SIZE,
        backupCount=BACKUP_COUNT
    )
    file_formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Optional: console handler
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter("[%(levelname)s] %(name)s | %(message)s")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger

def get_logger(context: str) -> logging.Logger:
    """
    Public interface to get a logger for a specific context (e.g., module or class name).
    """
    return configure_logger(context)
