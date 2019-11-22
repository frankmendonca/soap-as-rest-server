import time

from .logger import LoggerWrapper


_logger = LoggerWrapper()


# Calcula o tempo de execucao da chamada do metodo
def elapsed(func):
    def wrapper(*args, **kargs):
        start = time.time()
        try:
            ret = func(*args, **kargs)
        finally:
            end = time.time()
            elapsed_time = round((end - start) * 1000)
            _logger.debug('Demorou: %sms', elapsed_time)
        return ret

    return wrapper
