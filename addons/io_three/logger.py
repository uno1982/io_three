import os
import logging
import tempfile

from . import constants

LOG_FILE = None
LOGGER = None

level_map = {
    constants.DISABLED: logging.NOTSET,
    constants.DEBUG: logging.DEBUG,
    constants.INFO: logging.INFO,
    constants.WARNING: logging.WARNING,
    constants.ERROR: logging.ERROR,
    constants.CRITICAL: logging.CRITICAL
}

def init(filename, level=constants.DEBUG):
    """Initialize the logger.

    :param filename: base name of the log file
    :param level: logging level (Default value = DEBUG)

    """
    global LOG_FILE
    LOG_FILE = os.path.join(tempfile.gettempdir(), filename)
    with open(LOG_FILE, 'w'):
        pass

    global LOGGER
    LOGGER = logging.getLogger('Three.Export')

    # Handle EnumProperty objects
    if isinstance(level, dict) and 'default' in level:
        level = level['default']
    elif hasattr(level, 'default'):
        level = level.default
    elif hasattr(level, 'get'):
        level = level.get('default', constants.DEBUG)
    
    # If level is still a complex object, try to extract the default value
    if not isinstance(level, str):
        if hasattr(level, 'items') and isinstance(level.items, list):
            level = level.items[0][0]  # Take the first item's identifier
        else:
            level = constants.DEBUG  # Fallback to DEBUG if we can't determine the level

    # Ensure level is a string
    level = str(level).lower()

    # Map the string level to the corresponding logging level
    level_map = {
        constants.DISABLED: logging.NOTSET,
        constants.DEBUG: logging.DEBUG,
        constants.INFO: logging.INFO,
        constants.WARNING: logging.WARNING,
        constants.ERROR: logging.ERROR,
        constants.CRITICAL: logging.CRITICAL
    }

    if level not in level_map:
        raise ValueError(f"Invalid logging level: {level}")

    log_level = level_map[level]
    LOGGER.setLevel(log_level)

    if not LOGGER.handlers:
        stream = logging.StreamHandler()
        stream.setLevel(log_level)

        format_ = '%(asctime)s - %(name)s - %(levelname)s: %(message)s'
        formatter = logging.Formatter(format_)

        stream.setFormatter(formatter)

        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)

        LOGGER.addHandler(stream)
        LOGGER.addHandler(file_handler)

def _logger(func):

    def inner(*args):
        if LOGGER is not None:
            func(*args)

    return inner


@_logger
def info(*args):
    LOGGER.info(*args)


@_logger
def debug(*args):
    LOGGER.debug(*args)


@_logger
def warning(*args):
    LOGGER.warning(*args)


@_logger
def error(*args):
    LOGGER.error(*args)


@_logger
def critical(*args):
    LOGGER.critical(*args)
