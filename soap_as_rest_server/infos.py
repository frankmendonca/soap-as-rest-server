from .logger import LoggerWrapper


def show_infos():
    import platform
    logger = LoggerWrapper()
    logger.info('Running on %s %s', platform.platform(), platform.architecture())
    logger.info('Python %s [%s / %s]', platform.python_version(), platform.python_implementation(),
                platform.python_compiler())
