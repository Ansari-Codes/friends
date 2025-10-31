from nicegui import ui, app
from ENV import THEME_DEFAULT
from utils.Auth import isAuthenticated

async def INIT_THEME():
    if not app.storage.user.get('theme'):
        app.storage.user.update({"theme": THEME_DEFAULT.copy()})
    theme = app.storage.user.get('theme', THEME_DEFAULT)
    colors = ui.colors(**theme)
    ui.dark_mode(False)
    ui.add_css("""
    .q-notification__message{
        font-size: 16px;
    }
    """, shared=True)
    return theme
