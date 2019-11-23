"""
Settings for application logging
"""
from datetime import datetime
import logging
import json
import time
import sys

from logging import handlers

from .settings import LOG_FILE, LOG_LEVEL, LOG_FORMAT

PIKA_LOGGING = logging.getLogger('pika')
PIKA_LOGGING.setLevel(logging.WARN)

REQUESTS_LOGGING = logging.getLogger('requests')
REQUESTS_LOGGING.setLevel(logging.WARN)

ZEEP_LOGGING = logging.getLogger('zeep')
ZEEP_LOGGING.setLevel(logging.WARN)


class CustomFormatter(logging.Formatter):
    def __init__(self):
        super(CustomFormatter, self).__init__()

    def format(self, record):
        message_object = {
            'level': record.levelname,
            'message': {
                'fileName': record.filename,
                'lineNumber': record.lineno,
                'appName': "soap-proxy",
                'message': record.msg,
            },
            'metadata': {
                'timestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
                'processName': sys.argv[0],
                **record,
            },
            'time': int(time.time())
        }

        if record.traceback:
            message_object['metadata']['traceback'] = record.traceback

        return json.dumps(message_object)


class CustomLogger(logging.Logger):
    """
    Custom logger implementation
    """

    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=None):
        if extra is None:
            extra = {}
        if 'traceback' not in extra:
            extra['traceback'] = ''
        if 'duration' not in extra:
            extra['duration'] = ''

        super(CustomLogger, self)._log(
            level, msg, args, exc_info, extra, stack_info)


logging.setLoggerClass(CustomLogger)
soap_proxy_logger = logging.getLogger('soap-proxy')
soap_proxy_logger.propagate = 0
soap_proxy_logger.setLevel(getattr(logging, LOG_LEVEL))


if LOG_FILE:
    SOAP_PROXY_HANDLER = handlers.RotatingFileHandler(
        LOG_FILE, maxBytes=100000000, backupCount=3)
    SOAP_PROXY_HANDLER.setFormatter(CustomFormatter())
    soap_proxy_logger.addHandler(SOAP_PROXY_HANDLER)

SOAP_PROXY_HANDLER = logging.StreamHandler()
SOAP_PROXY_HANDLER.setFormatter(logging.Formatter(
    LOG_FORMAT, datefmt='%Y-%m-%d %H:%M:%S'))

soap_proxy_logger.addHandler(SOAP_PROXY_HANDLER)


class LoggerWrapper:
    def __init__(self, prefix=''):
        self.prefix = f'[{prefix}] ' if prefix else ''

    def debug(self, msg, *args, **kwargs):
        soap_proxy_logger.debug(self.prefix + msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        soap_proxy_logger.info(self.prefix + msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        soap_proxy_logger.warning(self.prefix + msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        soap_proxy_logger.error(self.prefix + msg, *args, **kwargs)

    def exception(self, msg, *args, exc_info=True, **kwargs):
        # TODO to know whot use this with exception
        soap_proxy_logger.exception(self.prefix + msg, *args, exc_info, **kwargs)

    def critical(self, msg, *args, **kwargs):
        soap_proxy_logger.critical(self.prefix + msg, *args, **kwargs)
