from nicegui import ui
from UI import Label, Row, RawCol, RawRow, Col, Icon, SoftBtn, AddSpace
from ENV import THEME_DEFAULT, APP_NAME, FAVICON

def CompInterfaceWelcome():
    with Col(
        "items-center justify-center w-[96vw] lg:w-[75vw] h-[95vh] p-10 text-center gap-4 rounded-xl",
        styles=f"background: linear-gradient(to right, {THEME_DEFAULT['primary']}, #ffffff, {THEME_DEFAULT['secondary']});"
    ):
        with Row('w-full items-center justify-center select-none'):
            Label(FAVICON, f"text-9xl border-4 border-[{THEME_DEFAULT.get('primary', '#147914')}] py-7 bg-secondary rounded-full")
            with RawCol('w-fit h-fit gap-0'):
                Label(APP_NAME, "text-9xl font-extrabold")
                with RawRow("w-full"):
                    Label(
                        "Connections that last a lifetime!",
                        "text-sm sm:text-lg p-1 rounded-sm w-fit md:w-[45%] italic",
                        )
