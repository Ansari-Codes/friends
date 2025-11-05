from UI import LabeledInput, Card, Center, Label, INIT_THEME, SoftBtn, Notify, Link
from library.formHandler import Variable, Group
from backend import ControlAuth
from utils.Storage import updateUserStorage
from utils import navigate
from routes import ROUTES
from nicegui import ui

async def signup(form, errs, widgets_to_disable: list[ui.input]):
    data = form.to_dict()
    for i in widgets_to_disable:
        i.disable()
    response = await ControlAuth.create(data)
    if response.get("success"): 
        updateUserStorage({k:v for k,v, in response.get("data", {})[0].items() if k!="password"})
        updateUserStorage({"auth":True})
        navigate(ROUTES.MAIN)
    else:
        errors = response.get("errors", {})
        errs.name.value = errors.get("name", "")
        errs.email.value = errors.get("email", "")
        errs.password.value = errors.get("password", "")
        if errors.get("unknwon"):
            Notify(errors.get("unknown"), type="error")
    for i in widgets_to_disable:
        i.enable()

def initialize_forms():
    form_variables = [
        Variable("name", ""),
        Variable("email", ""),
        Variable("password", ""),
        Variable("confirm", ""),
    ]
    errs_variables = [
        Variable("name", ""),
        Variable("email", ""),
        Variable("password", ""),
        Variable("confirm", ""),
    ]

    form = Group(form_variables)
    errs = Group(errs_variables)
    return form, errs, [
    [
        dict(
            name = dict(
                text = "Name *",
                clas = "text-lg font-bold",
                err  = errs.name
            )
        ),
        dict(
            name = dict(
                placeholder = "Dispaly name...",
                model = form.name,
                bindings = {
                    "forward": lambda x: str(x or "").lower()
                }
            )
        ),
    ],
    [
        dict(
            email = dict(
                text = "Email *",
                clas = "text-lg font-bold",
                err  = errs.email
            )
        ),
        dict(
            email = dict(
                placeholder = "Email...",
                model = form.email,
                bindings = {
                    "forward": lambda x: str(x or "").lower()
                }
            )
        ),
    ],
    [
        dict(
            password = dict(
                text = "Password *",
                clas = "text-lg font-bold",
                err  = errs.password
            )
        ),
        dict(
            password = dict(
                placeholder = "Password...",
                password = True,
                password_toggle_button = True,
                clas="mb-2",
                model = form.password,
            ),
            confirm = dict(
                placeholder = "Confirm...",
                password = True,
                password_toggle_button = True,
                model = form.confirm
            )
        ),
    ]
]

def _dict_to_widget(l):
    widgets = []
    for i in l:
        widgets.extend(list(i.get("inputs", {}).values()))
    return widgets

async def create():
    await INIT_THEME()
    form, errs, inputs_and_labels = initialize_forms()
    with Center(clas="w-full h-full"):
        with Card("max-w-md w-full h-fit flex flex-col"):
            Label("Sign Up", "w-full border-b-2 text-2xl font-bold text-center")
            labels_and_inputs = []
            for i in inputs_and_labels:
                labels_and_inputs.append(LabeledInput(*i))
            SoftBtn("Create Account", lambda: signup(form, errs, _dict_to_widget(labels_and_inputs)), clas="w-full")
            Link('Or Login here...', ROUTES.LOGIN)
