from UI import RawCol, RawRow, Label, Input, Icon, AddSpace, Row, Col, SoftBtn
from backend.Controllers.ControlContacts import get_contacts
from utils.Storage import getUserStorage
from nicegui.ui import button_group
from ENV import THEME_DEFAULT
from library.formHandler import Variable

async def create_search(contacts: list, model: Variable):
    names = [i.get("user", {}).get("name") for i in contacts]
    with Row(f"w-full border border-[{THEME_DEFAULT.get('primary', '#0f0')}] rounded-sm gap-0") as cont:
        Input(
            "flex flex-grow flex-shrink px-2 bg-transparent", 
            autocomplete = names,
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

async def list_contacts(contacts, model:Variable):
    contcts = []
    with RawCol('w-full h-fit max-h-full overflow-y-auto') as container:
        for i in contacts:
            widget = SoftBtn(
                    i.get("user", {}).get("name"),
                    on_click=lambda value=i: model.setValue(value),
                    clr="primary",
                    clas="w-full text-left"
                )
            contcts.append({
                'btn': widget,
                'contact': i
            })
    return contcts, container

async def CompSideBar():
    response = (await get_contacts(getUserStorage().get("id"))) or {}
    contacts = response.get("data", [])
    await create_search(contacts, Variable("query"))
    await list_contacts(contacts, Variable("selected"))
