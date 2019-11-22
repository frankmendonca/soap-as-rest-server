from tornado.web import RequestHandler
from requests.exceptions import ConnectTimeout
import traceback
import json

from . import soap_client
from .settings import SERVER_ENDPOINT
from .config import endpoints
from .logger import LoggerWrapper

ACCEPT_CONTENT_JSON = 'application/json'
ACCEPT_CONTENT_XML = 'text/xml'


class MainHandler(RequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = LoggerWrapper('MainHandler::post')

    def get(self, endpoint):
        path = endpoint.replace(SERVER_ENDPOINT, '')
        if path == 'health':
            logger_health = LoggerWrapper('MainHandler::get::health')
            logger_health.info('Called Health')
            self.set_status(200)
            self.write("OK")
        else:
            super(MainHandler, self).get(endpoint)

    def post(self, endpoint):
        path = endpoint.replace(SERVER_ENDPOINT, '')
        self.logger.info('Endpoint = %s', path)

        endpoint_config = endpoints.get(path)

        if not endpoint_config:
            self.set_status(404)
            return

        self.logger.info("config = %s", endpoint_config)
        self.logger.info("body = %s", self.request.body)

        accept_xml = is_accept_xml(self.request)

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


def is_accept_xml(request):
    return request.headers.get('Accept', ACCEPT_CONTENT_JSON) == ACCEPT_CONTENT_XML


def build_soap_config(endpoint_config, request_body, accept_xml):
    soap_config = endpoint_config.copy()
    soap_config['accept_xml'] = accept_xml

    if request_body:
        body = json.loads(request_body)
        soap_config['params'] = body
    else:
        soap_config['params'] = {}

    return soap_config
