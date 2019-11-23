def set_header_handler(handler):
    print('setting handler...')
    global headerHandler
    headerHandler = handler


def get_values():
    if 'headerHandler' in globals():
        global headerHandler
        return headerHandler.generate_values()
    return {}
