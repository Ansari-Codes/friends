from .ROUTES import LOGIN, SIGNUP, createLoadingScreen
from nicegui.ui import page
from pages.Auth.PageSignUp import create as create_signup
from pages.Auth.PageLogin import create as create_login
from ENV import APP_NAME

@page(LOGIN, title=APP_NAME + " - Login")
async def render_login():
    await createLoadingScreen(create_login, auth=False)

@page(SIGNUP, title=APP_NAME + " - SignUp")
async def render_signup():
    await createLoadingScreen(create_signup, auth=False)
