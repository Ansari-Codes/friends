from nicegui import ui
from UI import Label, Raw, Row, RawCol, RawRow, Col, Icon, SoftBtn, AddSpace, Card, Center
from ENV import THEME_DEFAULT, APP_NAME, FAVICON, QUOTE

def CompInterfaceWelcome():
    with Col(
        "items-center justify-center w-[96vw] lg:w-[75vw] h-[94vh] p-10 text-center gap-4 rounded-xl"
    ):
        with Center('w-full'):
            with Row("w-full h-full gap-2 items-center justify-center"):
                Label(
                    FAVICON,
                    f'text-8xl sm:text-9xl py-6 rounded-full '
                    f'border-6 border-[{THEME_DEFAULT.get("primary", "#1d5c1d")}] '
                    f'bg-secondary',
                )
                with Col():
                    Label(
                        APP_NAME, 
                        "text-7xl sm:text-9xl font-extrabold"
                    )
                    if QUOTE:
                        Label(
                            QUOTE,
                            "text-sm sm:text-lg italic",
                        )
