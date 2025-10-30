from UI import Raw, SoftBtn, Label, Button, INIT_THEME, Header, Icon, Row
from UI.Basic import Footer
from utils.Storage import clearUserStorage
from utils import navigate
from library.formHandler import Variable
from comps.Interface import CompChat, CompInterfaceWelcome, CompSideBar
from nicegui.ui import element, left_drawer, header, add_css
from comps.CompHeaderTitle import CompHeaderTitle
from backend.Models.ModelAuth import Auth
from ENV import APP_NAME
from nicegui.ui import context

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
        await CompChat.CompChat(contact, chat_box, drawer, header, footer)
    page_layout = context.client.layout
    page_layout.props(remove='view', add='view="lHh lpR lFf"')
    header = Header()
    with left_drawer().classes("bg-secondary") as drawer : await CompSideBar.CompSideBar(query_model, open_chat)
    footer = Footer()
    with Raw.RawCol("w-full h-fit gap-1"):
        chat_box = element('div').classes(
            'flex flex-col w-full h-fit justify-center '
            'items-center '
            )
        with chat_box:
            await CompInterfaceWelcome.CompInterfaceWelcome(drawer)
            header.set_visibility(False)
            footer.set_visibility(False)
