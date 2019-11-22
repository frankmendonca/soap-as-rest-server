def start():
    from .infos import show_infos
    from . import app

    show_infos()
    app.init()
