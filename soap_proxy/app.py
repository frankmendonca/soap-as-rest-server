from tornado.ioloop import IOLoop
from tornado.web import Application

from .settings import SERVER_PORT, SERVER_ENDPOINT
from .main_handler import MainHandler
from .logger import LoggerWrapper


def make_app():
    return Application([
        (f"{SERVER_ENDPOINT}(\\w+)", MainHandler),
    ])


def init():
    logger = LoggerWrapper()
    app = make_app()
    logger.info('Application starting on port %s and enpoint "%s"...', SERVER_PORT, SERVER_ENDPOINT)
    app.listen(SERVER_PORT)
    logger.info('Application started !')
    IOLoop.current().start()
