from utils import navigate
from utils.Auth import isAuthenticated
from nicegui import ui, app
from UI import Raw, Col, Row, THEME_DEFAULT
import asyncio

MAIN = '/'
LOGIN = '/login'
SIGNUP = '/signup'

async def createLoadingScreen(
        page, 
        *,
        auth=True, 
        if_not_auth=None, 
        if_not_auth_kwargs: dict|None = None,
        kwargs: dict|None = None,
    ):
    kwargs = kwargs or {}
    theme = app.storage.user.get("theme", THEME_DEFAULT.copy())
    with Col('w-[95vw] h-[95vh] justify-center items-center') as c:
        with Raw.RawRow('w-fit h-fit justify-center items-center'):
            ui.spinner("comment", size='80px', color=f'{theme.get("primary")}')
            Raw.Html(f"""
                <div class="flex flex-col">
                    <span class="text-[{theme.get('primary')}] text-3xl font-medium">
                        Loading
                    </span>
                    <span class="text-xs text-gray-400">
                        Please Wait...
                    </span>
                </div>
            """)
    other_functions_is_to_be_called = False
    if auth:
        if not (await isAuthenticated()):
            if if_not_auth is not None:
                other_functions_is_to_be_called = True
            else:
                navigate(LOGIN)
    await ui.context.client.connected()
    c.delete()
    if other_functions_is_to_be_called:
        kwa = if_not_auth_kwargs or {}
        async def dummy(): return
        if_not_auth = if_not_auth or dummy
        await if_not_auth(**kwa)
    else:
        await page(**kwargs)
    return True
