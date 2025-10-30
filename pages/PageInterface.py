from UI import Raw, SoftBtn, Label, Button, INIT_THEME, Header, Icon, Row
from utils.Storage import clearUserStorage
from utils import navigate
from library.formHandler import Variable
from comps.Interface import CompChat, CompInterfaceWelcome, CompSideBar
from nicegui.ui import element, left_drawer, header, add_css
from comps.CompHeaderTitle import CompHeaderTitle
from backend.Models.ModelAuth import Auth
from ENV import APP_NAME

async def create():
    theme, _, _2 = await INIT_THEME()
    add_css(f"""
        body {{
            background: linear-gradient(
                135deg, 
                {theme['primary']} 0%, 
                {theme['primary']}88 40%,
                white 60%,
                {theme['secondary']} 100%
            );
        }}
    """)
    query_model = Variable("query")
    async def open_chat(contact: dict | None):
        contact = contact or {}
        chat_box.clear()
        await CompChat.CompChat(contact, chat_box, drawer)
    with left_drawer().classes("bg-secondary") as drawer : await CompSideBar.CompSideBar(query_model, open_chat)
    with Raw.RawCol("w-full h-fit gap-1"):
        chat_box = element('div').classes(
            'flex flex-col w-full h-full justify-center '
            'items-center overflow-hidden '
            )
        with chat_box:
            await CompInterfaceWelcome.CompInterfaceWelcome(drawer)
