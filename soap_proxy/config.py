import yaml
from .settings import CONFIG_FILE
from .logger import LoggerWrapper

endpoints = ''


def load():
    global endpoints
    logger = LoggerWrapper()

    try:
        logger.debug('Loading "%s"...', CONFIG_FILE)
        with open(CONFIG_FILE, 'r') as config_file:
            config = yaml.safe_load(config_file)
            endpoints = config.get('endpoints', {})
    except Exception as e:
        logger.error('File "%s" not found', CONFIG_FILE)
        raise Exception('File "%s" not found', CONFIG_FILE)


load()
