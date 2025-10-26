from .ROUTES import MAIN, isAuthenticated
from nicegui.ui import page
from pages.PageWelcome import create as create_welcome
from pages.PageInterface import create as create_interface

@page(MAIN)
async def render_main():
    if not isAuthenticated():
        await create_welcome()
    else:
        await create_interface()
