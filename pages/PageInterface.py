from UI import Raw, SoftBtn, Label, Button, INIT_THEME, Header, Icon, Row
from utils.Storage import clearUserStorage
from utils import navigate
from library.formHandler import Variable
from comps.Interface import CompChat, CompSideBar
from nicegui.ui import element, left_drawer, header, sub_pages
from comps.CompHeaderTitle import CompHeaderTitle
from backend.Models.ModelAuth import Auth

def toggleDrawer(drawer: left_drawer):
    drawer.toggle()
    s = drawer.value
    to_add = ""
    if s:
        pass

async def create():
    INIT_THEME()
    query_model = Variable("query")
    select_model = Variable("select", {})
    with left_drawer().classes("bg-secondary"):
        await CompSideBar.CompSideBar(query_model, select_model)
    with Header(clas='bg-primary justify-between items-center'):
        CompHeaderTitle()
        SoftBtn("LogOut", on_click=lambda: [clearUserStorage(), navigate('/')])
    sub_pages({
        "/contact/{id_}":lambda id_: CompChat.CompChat(Auth().getUserById(id_))
    })
    