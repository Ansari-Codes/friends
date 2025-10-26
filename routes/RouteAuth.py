from .ROUTES import LOGIN, SIGNUP, isAuthenticated
from nicegui.ui import page
from pages.Auth.PageSignUp import create as create_signup
from pages.Auth.PageLogin import create as create_login
from utils import navigate

@page(LOGIN)
async def render_login():
    if isAuthenticated():navigate("/")
    await create_login()

@page(SIGNUP)
async def render_signup():
    if isAuthenticated():navigate("/")
    await create_signup()
