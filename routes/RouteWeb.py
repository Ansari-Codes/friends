from .ROUTES import MAIN, createLoadingScreen
from nicegui.ui import page
from pages.PageWelcome import create as create_welcome
from pages.PageInterface import create as create_interface
from ENV import APP_NAME

@page(MAIN, title=APP_NAME)
async def render_main():
    await createLoadingScreen(create_interface, if_not_auth=create_welcome)
