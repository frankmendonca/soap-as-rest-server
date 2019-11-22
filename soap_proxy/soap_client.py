import requests

from .config import endpoints
from .elapsed import elapsed
from .json_converter import convert_xml_to_json
from .template_helper import template_body
from .xml_converter import convert_json_to_xml
from .logger import LoggerWrapper

HEADERS = {'content-type': 'text/xml'}

_logger = LoggerWrapper('SOAP_PROXY::send_request')


def send_request(soap):
    host = soap.get('host')
    service = soap.get('service')
    service_namespace = soap.get('service_namespace', service)
    method = soap.get('method')
    params = soap.get('params')
    timeout = soap.get('timeout', endpoints.get('timeout'))
    accept_xml = soap.get('accept_xml')

    url = f'{host}/{service}?wsdl'
    _logger.debug("URL = %s", url)

    body = convert_json_to_xml('con', method, params)
    data = build_body_from_template(service_namespace, body)
    _logger.info("Request data: %s", data)

    response = call_post(url, data, timeout)

    _logger.info("Response data: %s", response)
    _logger.debug('Response[content] = %s', response.content)
    _logger.debug('Response[status_code] = %s', response.status_code)

    if accept_xml:
        response.translated_response = response.content
    else:
        response.translated_response = convert_xml_to_json(response.content)

    _logger.info('Response[translated] = %s', response.translated_response)

    return response


def build_body_from_template(service_namespace, body):
    return template_body.format(service=service_namespace, body=body)


@elapsed
def call_post(url, data, timeout):
    return requests.post(url=url, data=data, headers=HEADERS, timeout=timeout, verify=False)
