from nicegui import ui, app
from ENV import THEME_DEFAULT
from utils.Auth import isAuthenticated

def INIT_THEME():
    if not (app.storage.user.get('theme') and isAuthenticated()):
        app.storage.user.update({"theme": THEME_DEFAULT.copy()})
    else:
        app.storage.user.update({"theme": THEME_DEFAULT.copy()})
    theme = app.storage.user.get('theme', THEME_DEFAULT)
    colors = ui.colors(**theme)
    mode = app.storage.user.get('dark', None)
    moder = ui.dark_mode(mode)
    def change(value):
        moder.value = value
    return colors, moder, change
