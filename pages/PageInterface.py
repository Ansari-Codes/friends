from UI import Raw, SoftBtn, Label, Button, INIT_THEME, Header, Icon, Row, Notify
from UI.Basic import Footer
from utils.Storage import clearUserStorage
from utils import navigate
from library.formHandler import Variable
from comps.Interface import CompChat, CompInterfaceWelcome, CompSideBar, CompTheme
from nicegui.ui import element, left_drawer, header, add_css, query
from comps.CompHeaderTitle import CompHeaderTitle
from backend.Models.ModelAuth import Auth
from ENV import APP_NAME
from nicegui.ui import context

def setupLayout(header, footer, container):
    page_layout = context.client.layout
    page_layout.props(remove='view', add='view="lHh lpR lFf"')
    container.clear()
    header.clear()
    footer.clear()
    header.set_visibility(True)
    footer.set_visibility(True)

async def create():
    theme = await INIT_THEME()
    query("body").element.classes("")
    add_css(f"""
        body {{
    background: linear-gradient(
        135deg,
        var(--q-primary) 0%,
        var(--q-accent) 50%,
        var(--q-secondary) 100%
    );
        }}
    """)
    query_model = Variable("query")
    def setup():
        setupLayout(header, footer, chat_box)
    async def open_chat(contact: dict | None):
        contact = contact or {}
        setup()
        await CompChat.CompChat(contact, chat_box, drawer, header, footer)
    async def other_handler(c):
        if c == 'a': 
            Notify("I will do something here!", color="info")
            return
        elif c == 'u':
            setup()
            with chat_box:
                await CompTheme.CompTheme(header, footer, drawer)
    header = Header(
    ).props("dense"
    ).classes("bg-primary text-white flex items-center h-[7vh] p-0 px-2 space-x-0 space-y-0")
    with left_drawer().classes("bg-secondary") as drawer : await CompSideBar.CompSideBar(query_model, open_chat, other_handler)
    footer = Footer(
    ).classes("bg-primary text-white flex items-end min-h-[7vh] max-h-[500px] p-0 px-2 py-2 space-x-0 space-y-0"
    ).props("dense")
    with Raw.RawCol("w-full h-fit gap-1"):
        chat_box = element('div').classes(
            'flex flex-col w-full h-fit justify-center '
            'items-center '
            )
        with chat_box:
            await CompInterfaceWelcome.CompInterfaceWelcome(drawer)
            header.set_visibility(False)
            footer.set_visibility(False)
