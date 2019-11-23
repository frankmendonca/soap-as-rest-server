import json
import traceback

from requests.exceptions import ConnectTimeout

from . import soap_client
from .base_request_handler import BaseRequestHandler, ACCEPT_CONTENT_JSON
from .config_file import endpoints
from .logger import LoggerWrapper
from .settings import SERVER_ENDPOINT


class RestHandler(BaseRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = LoggerWrapper('RestHandler::post')

    def post(self, endpoint):
        path = endpoint.replace(f'{SERVER_ENDPOINT}api', '')
        self.logger.info('Endpoint = %s', path)

        endpoint_config = endpoints.get(path)

        if not endpoint_config:
            self.set_status(404)
            return

        self.logger.info("config = %s", endpoint_config)
        self.logger.info("body = %s", self.request.body)

        accept_xml = self.is_accept_xml()

        soap_config = build_soap_config(endpoint_config, self.request.body, accept_xml)

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


def build_soap_config(endpoint_config, request_body, accept_xml):
    soap_config = endpoint_config.copy()
    soap_config['accept_xml'] = accept_xml

    body = json.loads(request_body) if request_body else {}
    soap_config['params'] = body

    return soap_config
