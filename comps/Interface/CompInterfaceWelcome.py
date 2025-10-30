from nicegui import ui
from UI import Label, Raw, Row, RawCol, RawRow, Col, Icon, SoftBtn, AddSpace, Card, Center, INIT_THEME
from ENV import THEME_DEFAULT, APP_NAME, FAVICON, QUOTE

async def CompInterfaceWelcome(drawer):
    theme, *_ = await INIT_THEME()
    with Col(
        "items-center justify-center w-[96vw] lg:w-[75vw] h-[85vh] p-10 text-center gap-6 rounded-xl"
    ):
        # Main Logo + App Name
        with Center('w-full'):
            with Row("w-full h-full gap-4 items-center justify-center"):
                Label(
                    FAVICON,
                    f'text-8xl sm:text-9xl py-6 rounded-full '
                    f'border-6 border-[{theme.get("primary", "#1d5c1d")}] '
                    f'bg-secondary',
                )
                with Col("gap-2 items-center"):
                    Label(
                        APP_NAME, 
                        "text-7xl sm:text-9xl font-extrabold"
                    )
                    if QUOTE:
                        Label(
                            QUOTE,
                            "text-sm sm:text-lg italic text-primary",
                        )
                    SoftBtn("Open Contacts", on_click=lambda: drawer.set_value(True), clas="flex lg:hidden")
