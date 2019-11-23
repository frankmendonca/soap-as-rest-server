import json
import traceback

from requests.exceptions import ConnectTimeout
from tornado.web import RequestHandler

from . import soap_client
from .base_request_handler import BaseRequestHandler, ACCEPT_CONTENT_JSON
from .logger import LoggerWrapper
from .settings import TEST_ENDPOINT_ENABLED


class TestHandler(BaseRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = LoggerWrapper('TestHandler::post')

    def post(self, endpoint):
        if not TEST_ENDPOINT_ENABLED:
            super().post()
            return

        self.logger.info("body = %s", self.request.body)

        body = json.loads(self.request.body)
        accept_xml = self.is_accept_xml()

        soap_config = dict(
            host=body.get('host'),
            service=body.get('service'),
            service_namespace=body.get('serviceNamespace', body.get('service')),
            method=body.get('method'),
            params=body.get('params'),
            timeout=body.get('timeout'),
            accept_xml=accept_xml,
        )

        try:
            soap_response = soap_client.send_request(soap_config)

            if accept_xml:
                self.set_header('Content-Type', soap_response.headers['Content-Type'])
            else:
                self.set_header('Content-Type', ACCEPT_CONTENT_JSON)

            self.set_status(soap_response.status_code)
            self.write(soap_response.translated_response)
        except Exception as e:
            self.logger.error('Error = %s', e)
            traceback.print_exc()
            if isinstance(e, ConnectTimeout):
                self.set_status(408)  # Request Timeout
            else:
                self.set_status(500)  # Error
            self.write({'errorMessage': f'{e}', 'errorClass': type(e).__name__})


def clean_config(config):
    return {k: v for k, v in config.items() if v is not None and k != 'params'}
