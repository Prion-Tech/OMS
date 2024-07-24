import sys
import logging

from pythonjsonlogger import jsonlogger


LOG_FORMAT_DATETIME = '%Y-%m-%dT%H:%M:%S'
LOG_FORMAT_JSON = '%(levelname)s [%(record_id)s | %(request_id)s | %(asctime)s]: %(message)s'
LOG_FORMAT_STANDARD = '%(levelname)s [%(record_id)s | %(request_id)s | %(asctime)s]: %(message)s'


class LogFilter(logging.Filter):

    def filter(self, record):
        if not hasattr(record, 'record_id'):
            record.record_id = None
        if not hasattr(record, 'request_id'):
            record.request_id = None
        return True


def _setup_logging_json(level, stream, name):
    """Sets up JSON formatted logging.

    Args:
        level (int): Logging level, e.g., logging.INFO, logging.DEBUG.
        stream: Logging stream, e.g., sys.stdout, sys.stderr.
        name (str): Logging.logger name

    Returns:
        logging.Logger: Configured logger with JSON formatting.
    """

    logger = logging.getLogger(name)
    for handler in logger.handlers:
        logger.removeHandler(handler)
    for log_filter in logger.filters:
        logger.removeFilter(log_filter)

    logger.setLevel(level)

    handler = logging.StreamHandler(stream=stream)
    formatter = jsonlogger.JsonFormatter(fmt=LOG_FORMAT_JSON, datefmt=LOG_FORMAT_DATETIME)
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.addFilter(LogFilter())

    return logger


def _setup_logging_standard(level, stream, name):
    """Sets up standard formatted logging.

    Args:
        level (int): Logging level, e.g., logging.INFO, logging.DEBUG.
        stream: Logging stream, e.g., sys.stdout, sys.stderr.
        name (str): Logging.logger name

    Returns:
        logging.Logger: Configured logger with standard formatting.
    """

    logger = logging.getLogger(name)
    for handler in logger.handlers:
        logger.removeHandler(handler)
    for log_filter in logger.filters:
        logger.removeFilter(log_filter)

    logger.setLevel(level)

    handler = logging.StreamHandler(stream=stream)
    formatter = logging.Formatter(fmt=LOG_FORMAT_STANDARD, datefmt=LOG_FORMAT_DATETIME)
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.addFilter(LogFilter())

    return logger


def setup_logging(log_type: str = 'standard', log_level=logging.DEBUG, log_stream=sys.stderr, logger_name: str = __name__):
    """Configures logging for the application with either standard or JSON format.

    This function allows the user to choose between standard text-based logging and
    structured JSON logging. It configures the logging level and format based on
    the user's choice.

    Args:
        log_type (str, optional): The type of logging format, either 'standard' or 'json'. Defaults to 'standard'.
        log_level (logging.Level, optional): The logging level, such as logging.DEBUG or logging.INFO. Defaults to logging.DEBUG.
        log_stream: The logging stream, e.g., sys.stdout, sys.stderr.
        logger_name (str, optional): Name of logging.logger instance. Defaults to __name__.

    Returns:
        logging.Logger: The configured logger instance.
    """

    if log_type == 'standard':
        return _setup_logging_standard(level=log_level, stream=log_stream, name=logger_name)
    elif log_type == 'json':
        return _setup_logging_json(level=log_level, stream=log_stream, name=logger_name)
