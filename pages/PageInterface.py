from UI import Raw, SoftBtn, Label, Button, INIT_THEME, Header, Icon, Row
from utils.Storage import clearUserStorage
from utils import navigate
from library.formHandler import Variable
from comps.Interface import CompChat, CompInterfaceWelcome, CompSideBar
from nicegui.ui import element, left_drawer, header
from comps.CompHeaderTitle import CompHeaderTitle
from backend.Models.ModelAuth import Auth
from ENV import APP_NAME

async def create():
    INIT_THEME()
    query_model = Variable("query")
    async def open_chat(contact: dict | None):
        contact = contact or {}
        chat_box.clear()
        await CompChat.CompChat(contact, chat_box)
    with left_drawer().classes("bg-secondary"): await CompSideBar.CompSideBar(query_model, open_chat)
    with Raw.RawCol("w-fit h-fit gap-1"):
        chat_box = element('div').classes(
            'flex flex-col w-full h-full justify-center '
            'items-center overflow-hidden '
            )
        with chat_box: 
            CompInterfaceWelcome.CompInterfaceWelcome()
