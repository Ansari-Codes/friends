from UI import RawCol, RawRow, Label, Input, Icon, AddSpace, Row, Col, SoftBtn, Notify
from backend.Controllers.ControlContacts import get_contacts
from utils import navigate
from utils.Storage import getUserStorage
from nicegui.ui import button_group
from ENV import THEME_DEFAULT
from library.formHandler import Variable

async def add_contact():
    pass

async def list_contacts(contacts, open_chat_callback=None):
    contcts = []
    with RawCol('w-full h-fit max-h-full overflow-y-auto') as container:
        for i in contacts:
            def make_click_handler(contact):
                return lambda: open_chat_callback(contact) if open_chat_callback else None
            widget = SoftBtn(
                i.get("user", {}).get("name"),
                on_click=make_click_handler(i),
                clr="btn",
                clas="w-full hover:bg-primary gap-1",
                text_align='left',
                icon='person',
                justify=None,
            )
            contcts.append({
                'btn': widget,
                'contact': i
            })
    return contcts, container

async def createSearch(contacts: list, model: Variable):
    names = [i.get("user", {}).get("name") for i in contacts]
    with Row(f"w-full border border-[{THEME_DEFAULT.get('primary', '#0f0')}] rounded-sm gap-0") as cont:
        Input(
            "flex flex-grow flex-shrink px-2 bg-transparent", 
            autocomplete=names,
            props='dense borderless input-class="bg-transparent"',
            default_props=False,
            model=model,
        )
        SoftBtn(
            icon="search", 
            clas="bg-btn h-full w-fit shadow-none hover:shadow-none rounded-l-none",
            icon_config=dict(size="sm"),
            active_effects=True,
            hover_effects=True,
            px=2,
        )
    cont.classes("w-full")

async def createUISettings():
    widget = SoftBtn(
        text="THEME",
        clr="primary",
        text_align='left',
        justify=None,
        icon='colorize',
        clas="w-full hover:bg-primary gap-2 shadow-none",
    )
    return widget

async def createAccountSettings():
    widget = SoftBtn(
        text="PROFILE",
        clr="primary",
        text_align='left',
        icon='person_2',
        justify=None,
        clas="w-full hover:bg-primary gap-2 shadow-none",
    )
    return widget

async def createAddContact():
    widget = SoftBtn(
        text="ADD CONTACT",
        clr="primary",
        text_align='left',
        justify=None,
        icon='person_add',
        clas="w-full hover:bg-primary gap-2 shadow-none",
    )
    return widget

async def CompSideBar(model_query: Variable, open_chat_callback=None):
    response = (await get_contacts(getUserStorage().get("id"))) or {}
    contacts = response.get("data", [])
    await createSearch(contacts, model_query)
    await list_contacts(contacts, open_chat_callback)
    AddSpace()
    with RawCol('gap-1 w-full'):
        await createAddContact()
        await createAccountSettings()
        await createUISettings()
