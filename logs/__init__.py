from os import path, remove
import logging
import logging.config

if path.isfile('logs/logging.log'):
    remove('logs/logging.log')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger_file_handler = logging.FileHandler('logs/logging.log')
logger_file_handler.setLevel(logging.DEBUG)

logger_stream_handler = logging.StreamHandler()
logger_stream_handler.setLevel(logging.DEBUG)

logger_formatter = logging.Formatter('%(name)s - %(process)s- %(levelname)s - %(message)s')

logger_file_handler.setFormatter(logger_formatter)
logger_stream_handler.setFormatter(logger_formatter)

logger.addHandler(logger_file_handler)
logger.addHandler(logger_stream_handler)
logger.info('Настройка логгирования окончена!')