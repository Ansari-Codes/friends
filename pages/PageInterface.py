from UI import Raw, SoftBtn, Label, Button, INIT_THEME, Header, Icon, Row
from utils.Storage import clearUserStorage
from utils import navigate
from library.formHandler import Variable
from comps.Interface import CompChat, CompSideBar
from nicegui.ui import element, left_drawer, header
from comps.CompHeaderTitle import CompHeaderTitle

def toggleDrawer(drawer: left_drawer):
    drawer.toggle()
    s = drawer.value
    to_add = ""
    if s:
        pass

async def create():
    INIT_THEME()
    with left_drawer().classes("bg-secondary"):
        await CompSideBar.CompSideBar()
    with Header(clas='bg-primary justify-between items-center'):
        CompHeaderTitle()
        SoftBtn("LogOut", on_click=lambda: [clearUserStorage(), navigate('/')])
