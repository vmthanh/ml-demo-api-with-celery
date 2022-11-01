import os
import sys
import logging
from types import FrameType
from typing import cast

from loguru import logger

import config

loguru_setting = None


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
            frame = cast(FrameType, frame.f_back)
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


class LoguruSetting:
    def __init__(self):
        self.PROJECT_LOG_DIR = config.PROJECT_LOGS_DIR
        self.PROJECT_APP = config.PROJECT_APP
        self.log_configs = [
            {
                "level": "INFO",
                "filename": "info_{time:YYYY-MM-DD}.log",
                "rotation": "daily",  # new file is created each day at midnight
                "retention": "1 months",
                "formatter": "<level>{level: <8}</level>|<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>|<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>|<level>{message}</level>",
            },
            {
                "level": "DEBUG",
                "filename": "debug_{time:YYYY-MM-DD}.log",
                "rotation": "daily",  # new file is created each day at midnight
                "retention": "1 months",
                "formatter": "<level>{level: <8}</level>|<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>|<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>|<level>{message}</level>",
            },
            {
                "level": "ERROR",
                "filename": "error_{time:YYYY-MM-DD}.log",
                "rotation": "daily",  # new file is created each day at midnight
                "retention": "1 months",
                "formatter": "<level>{level: <8}</level>|<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>|<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>|<level>{message}</level>",
            },
        ]

    def customize_logging(self, level, filename, rotation, retention, formatter):
        # pylint: disable=unnecessary-lambda-assignment,too-many-arguments
        log_config_filter = lambda record: record["level"].name == f"{level}"
        ## Add log output to stdout
        logger.add(
            sys.stdout,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=formatter,
            filter=log_config_filter,
            colorize=True,
        )
        app_paths = self.PROJECT_APP.split(".")
        full_project_app_paths = os.path.join(
            self.PROJECT_LOG_DIR, *app_paths, filename
        )

        ## Add log output to file
        logger.add(
            str(full_project_app_paths),
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=formatter,
            rotation=rotation,
            retention=retention,
            filter=log_config_filter,
            colorize=False,
        )

    def setup_app_logging(self):
        """Prepare custom logging for our application."""
        logger.remove()
        for lc in self.log_configs:
            self.customize_logging(**lc)

        logging.basicConfig(handlers=[InterceptHandler()], level=logging.NOTSET)

        for _log in ["uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"]:
            _logger = logging.getLogger(_log)
            _logger.handlers = [InterceptHandler(level=logging.WARNING)]


if loguru_setting is None:
    loguru_setting = LoguruSetting()
