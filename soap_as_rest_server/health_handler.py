from tornado.web import RequestHandler

from .base_request_handler import BaseRequestHandler
from .logger import LoggerWrapper


class HealthHandler(BaseRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = LoggerWrapper('HealthHandler::get')

    def get(self):
        self.logger.info('Health called')
        self.set_status(200)
        self.write("OK")
