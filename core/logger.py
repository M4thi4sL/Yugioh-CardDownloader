import logging
import coloredlogs


def setup_logger():
    """
    Log messages with different levels
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')
    """
    logger = logging.getLogger(__name__)

    # Configure coloredlogs to format and colorize logs for the console
    coloredlogs.install(level="DEBUG", logger=logger, fmt="%(levelname)s: %(message)s")

    # Create a file handler to write logs to a log.txt file in the same folder (with mode 'w')
    file_handler = logging.FileHandler(".\\log.txt", mode="w")

    # Configure the log format for the file handler (customize as needed)
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    return logger


def set_log_level(logger, log_level):
    """
    Sets the logging level for the logger.

    Parameters:
    - logger (logging.Logger): The logger instance.
    - log_level (int): The logging level to set.
    """
    logger.setLevel(log_level)


# Configure and return the logger
logger = setup_logger()
