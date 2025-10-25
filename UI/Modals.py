from nicegui import ui


def Notify(message:str = '', **kwargs):
    ui.notify(message, position='top-right', **kwargs)
