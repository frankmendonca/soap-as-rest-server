from tornado.ioloop import IOLoop
from tornado.web import Application

from .settings import SERVER_PORT, SERVER_ENDPOINT
from .health_handler import HealthHandler
from .rest_handler import RestHandler
from .test_handler import TestHandler
from .logger import LoggerWrapper


def routes():
    return [
        (f"{SERVER_ENDPOINT}health", HealthHandler),
        (f"{SERVER_ENDPOINT}rest/(\\w+)", RestHandler),
        (f"{SERVER_ENDPOINT}test/(\\w+)", TestHandler),
    ]


def make_server():
    return Application(routes())


def init():
    logger = LoggerWrapper()
    server = make_server()
    logger.info('Application starting on port %s and enpoint "%s"...', SERVER_PORT, SERVER_ENDPOINT)
    server.listen(SERVER_PORT)
    logger.info('Application started !')
    IOLoop.current().start()
