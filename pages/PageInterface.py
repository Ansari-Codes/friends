from UI import Raw, SoftBtn, Label, Button, INIT_THEME, Header
from utils.Storage import clearUserStorage
from utils import navigate
from library.formHandler import Variable
from comps.Interface import CompChat
from nicegui.ui import left_drawer, header

async def create():
    INIT_THEME()
    with left_drawer().classes("bg-primary"):
        pass
    with Header(clas="bg-secodary", props="view-l"):
        pass
    SoftBtn("LogOut", on_click=lambda: [clearUserStorage(), navigate('/')])
