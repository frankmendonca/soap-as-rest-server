def start():
    from .infos import show_infos
    from . import server

    show_infos()
    server.init()
