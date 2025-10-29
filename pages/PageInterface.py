from UI import Raw, SoftBtn, Label, Button, INIT_THEME, Header, Icon, Row
from utils.Storage import clearUserStorage
from utils import navigate
from library.formHandler import Variable
from comps.Interface import CompChat, CompSideBar
from nicegui.ui import element, left_drawer, header
from comps.CompHeaderTitle import CompHeaderTitle
from backend.Models.ModelAuth import Auth

async def create():
    INIT_THEME()
    query_model = Variable("query")
    async def open_chat(contact: dict | None):
        contact = contact or {}
        chat_box.clear()
        await CompChat.CompChat(contact, chat_box)
    with left_drawer().classes("bg-secondary"):
        await CompSideBar.CompSideBar(query_model, open_chat)
    # with Header(clas='bg-primary justify-between items-center'):
    #     CompHeaderTitle()
    #     SoftBtn("LogOut", on_click=lambda: [clearUserStorage(), navigate('/')])
    chat_box = element('div').classes('flex flex-col w-full h-full')
    with chat_box: Label('Select a contact from the sidebar to start chatting')
