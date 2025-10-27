from UI import RawCol, RawRow, Label, Input, Icon, AddSpace, Row, Col, SoftBtn
from backend.Controllers.ControlContacts import get_contacts
from utils.Storage import getUserStorage

def create_search(contacts):
    names = [i.get("user", {}).get("name") for i in contacts]
    with RawRow("w-full h-fit items-center") as cont:
        with Input("flex flex-grow flex-shrink", autocomplete = names):
            SoftBtn(
                icon="search", 
                clas="bg-btn h-full w-fit shadow-none hover:shadow-none rounded-l-none",
                icon_config=dict(size="sm"),
                active_effects=True,
                hover_effects=True,
                px=2
                )

async def CompSideBar():
    response = (await get_contacts(getUserStorage().get("id"))) or {}
    contacts = response.get("data", [])
    return create_search(contacts)

