from tornado.web import RequestHandler


ACCEPT_CONTENT_JSON = 'application/json'
ACCEPT_CONTENT_XML = 'text/xml'


class BaseRequestHandler(RequestHandler):
    def is_accept_xml(self):
        return self.request.headers.get('Accept', ACCEPT_CONTENT_JSON) == ACCEPT_CONTENT_XML
