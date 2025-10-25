from .ROUTES import MAIN, DASHBOARD, require_auth
from nicegui.ui import page
from pages.PageWelcome import create as create_welcome
from pages.PageDashboard import create as create_dashboard

@page(MAIN)
async def render_main():
    await create_welcome()

@page(DASHBOARD)
@require_auth
async def render_dashboard():
    await create_dashboard()
