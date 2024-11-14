import logging
import logging.handlers


def setup_logger(name, level=logging.DEBUG):
    """Set up a logger that writes to both a log file and the console."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.hasHandlers():
        file_handler = logging.handlers.RotatingFileHandler(
            name,
            maxBytes=1024 * 1024,
            backupCount=1,
            encoding="utf8",
        )
        file_handler.setLevel(level=level)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level=level)
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    return logger


logger = setup_logger(name="weather.log")