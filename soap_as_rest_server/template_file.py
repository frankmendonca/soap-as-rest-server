from .settings import TEMPLATE_FILE
from .logger import LoggerWrapper

template_body = ''


def load():
    global template_body
    logger = LoggerWrapper()

    try:
        logger.debug('Loading "%s"...', TEMPLATE_FILE)
        with open(TEMPLATE_FILE, 'r') as reader:
            template_body = ''.join(line for line in reader)
    except Exception as e:
        logger.error('File "%s" not found', TEMPLATE_FILE)
        raise Exception('File "%s" not found', TEMPLATE_FILE)


load()
