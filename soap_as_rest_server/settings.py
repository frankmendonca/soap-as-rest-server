from os import environ


# files
CONFIG_FILE = environ.get('CONFIG_FILE') # e.g.: config.yml
TEMPLATE_FILE = environ.get('TEMPLATE_FILE') # e.g.: template.xml

# server
SERVER_PORT = int(environ.get('SERVER_PORT', '3333'))
SERVER_ENDPOINT = environ.get('SERVER_ENDPOINT', '/') # e.g.: /myserver/

# log
LOG_FILE = environ.get('LOG_FILE', 'False') == 'True'
LOG_LEVEL = environ.get('LOG_LEVEL', 'DEBUG')
LOG_FORMAT = environ.get('LOG_FORMAT',
                         '%(asctime)s|%(name)s|%(message_key)s|%(retries)s|%(levelname)s: %(message)s|%(duration)s')
