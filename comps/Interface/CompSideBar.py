from UI import RawCol, RawRow, Label, Input, Icon, AddSpace, Row, Col, SoftBtn, Notify, DialogHeader, Card, Div
from backend.Controllers.ControlContacts import get_contacts, get_All_users
from backend.Controllers import ControlChat
from backend.Models.ModelAuth import Auth
from utils import navigate
from utils.Storage import getUserStorage
from ENV import THEME_DEFAULT
from library.formHandler import Variable
from nicegui.ui import dialog as dial
from utils.Storage import getUserStorage

async def __send_inv(user: str, dialog, contacts, lister, contcts, open_chat_callback):
    user_ = await Auth().getUserByIdentifier(user.strip().lower())
    response = await ControlChat.send({
        "from_id": getUserStorage().get("id"),
        "to_id": user_[0].get("id"),
        "content": "Assalam-o-Alaikum!\n😁😁😁😁😁😁😁"
    })
    u = user_[0]
    u.pop("password", None)
    m = response.get("data")
    if response.get("success"):
        contact = {
            "user": user_[0],
            "messages": m
        }
        contacts.append(contact)
        def make_click_handler(contact):
            return lambda: open_chat_callback(contact) if open_chat_callback else None
        widget = SoftBtn(
            u.get("name", "UNKNOWN"),
            on_click=make_click_handler(contact),
            clr="btn",
            clas="w-full hover:bg-primary gap-1",
            text_align='left',
            icon='person',
            justify=None,
        )
        contcts.append({
            'btn': widget,
            'contact': contact
        })
        widget.move(lister)
    else:
        Notify(response.get("errors",{}).get("unknown", "Sorry, an unknown error occured!"), color='error', icon='error')
    dialog.close()

async def add_contact(dialog: dial, contacts: list, lister, cntcts, mch):
    all_users = await get_All_users()
    all_users = all_users.get("data", [])
    add_contact_model = Variable("name")
    dialog.clear()
    dialog.props('persistent="false"')
    with dialog:
        with Card('p-0 m-0'):
            with Div('w-full h-full'):
                DialogHeader(title="Add Contact", on_close=dialog.close)
                with RawCol('p-2 m-0 gap-2'):
                    Input(
                        "w-full flex flex-grow flex-shrink",
                        autocomplete=[i.get("name") for i in all_users],
                        model=add_contact_model
                    )
                    SoftBtn(
                        "Add",
                        icon="add",
                        on_click=lambda a=add_contact_model, d=dialog, c=contacts, l=lister, cc=cntcts, mch=mch: (
                            __send_inv(a.value, d, c, l, cc, mch)
                        )
                    )
    dialog.open()

async def list_contacts(contacts, open_chat_callback=None):
    contcts = []
    with RawCol('w-full h-fit max-h-full overflow-y-auto gap-1') as container:
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

async def createAddContact(dialog, contacts, lister, cntcts, mch):
    widget = SoftBtn(
        text="ADD CONTACT",
        clr="primary",
        text_align='left',
        justify=None,
        icon='person_add',
        clas="w-full hover:bg-primary gap-2 shadow-none",
        on_click=lambda d=dialog, c=contacts, l=lister, cc=cntcts, mch=mch: add_contact(d, c, l, cntcts, mch)
    )
    return widget

async def CompSideBar(model_query: Variable, open_chat_callback=None):
    response = (await get_contacts(getUserStorage().get("id"))) or {}
    contacts = response.get("data", [])
    await createSearch(contacts, model_query)
    cntcts,lister = await list_contacts(contacts, open_chat_callback)
    dialog = dial()
    AddSpace()
    with RawCol('gap-1 w-full'):
        await createAddContact(dialog, contacts, lister, cntcts, open_chat_callback)
        await createAccountSettings()
        await createUISettings()
