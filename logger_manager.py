import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

from colorlog import ColoredFormatter


class LoggerManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)        
        self._setup_console_handler()

    def _setup_console_handler(self):
        console_handler = logging.StreamHandler()
        formatter = ColoredFormatter(
            "[%(asctime)s] [%(log_color)s%(levelname)s%(reset)s] - %(message)s",
            datefmt=None,
            reset=True,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'purple',
            },
            secondary_log_colors={},
            style='%'
        )
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def debug(self, message):
        """
        Логгирование сообщения уровня DEBUG.

        Parameters:
            message (str): Сообщение для логирования.
        """
        self.logger.debug(message)

    def info(self, message):
        """
        Логгирование сообщения уровня INFO.

        Parameters:
            message (str): Сообщение для логирования.
        """
        self.logger.info(message)

    def warning(self, message):
        """
        Логгирование сообщения уровня WARNING.

        Parameters:
            message (str): Сообщение для логирования.
        """
        self.logger.warning(message)

    def error(self, message):
        """
        Логгирование сообщения уровня ERROR.

        Parameters:
            message (str): Сообщение для логирования.
        """
        self.logger.error(message)

    def critical(self, message):
        """
        Логгирование сообщения уровня CRITICAL.

        Parameters:
            message (str): Сообщение для логирования.
        """
        self.logger.critical(message)

    def print_separator(self):
        """
        Вывод разделительного сообщения в консоль.
        """
        separator = "=" * 40
        print(separator)
