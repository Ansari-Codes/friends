from .ROUTES import LOGIN, SIGNUP
from nicegui.ui import page
from pages.Auth.PageSignUp import create as create_signup
from pages.Auth.PageLogin import create as create_login

@page(LOGIN)
async def render_login():
    await create_login()

@page(SIGNUP)
async def render_signup():
    await create_signup()
