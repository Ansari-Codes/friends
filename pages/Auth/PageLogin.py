from UI import LabeledInput, Card, Center, Label, INIT_THEME, SoftBtn, Notify, Link
from library.formHandler import Variable, Group
from backend import ControlAuth
from utils.Auth import updateUserStorage
from utils import navigate
from routes import ROUTES

async def login(form, errs):
    data = form.to_dict()
    response = await ControlAuth.login(data)
    if response.get("success"):
        updateUserStorage({k:v for k,v in response.get("data", {}).items() if k not in ["created_at", "updated_at", "password"]})
        updateUserStorage({'auth': True})
        navigate('/')
    else:
        errors = response.get("errors", {})
        errs.identifier.value = errors.get("identifier", "")
        errs.password.value = errors.get("password", "")
        if errors.get("unknown"):
            Notify(errors.get("unknown"), color='error')

def initialize_forms():
    form_variables = [
        Variable("identifier", ""),
        Variable("password", ""),
    ]
    errs_variables = [
        Variable("identifier", ""),
        Variable("password", ""),
    ]
    form = Group(form_variables)
    errs = Group(errs_variables)
    inputs_and_labels = [
        [
            dict(
                email = dict(
                    text = "Email/Name *",
                    clas = "text-lg font-bold",
                    err  = errs.identifier
                )
            ),
            dict(
                email = dict(
                    placeholder = "Your email or name...",
                    model = form.identifier,
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
            )
        ]
    ]
    return form, errs, inputs_and_labels

async def create():
    INIT_THEME()
    form, errs, inputs_and_labels = initialize_forms()
    with Center(clas="w-full h-full"):
        with Card("max-w-md w-full h-fit flex flex-col"):
            Label("Login", "w-full border-b-2 text-2xl font-bold text-center")
            for i in inputs_and_labels:
                LabeledInput(*i)
            SoftBtn("Login", lambda:login(form, errs), clas="w-full")
            Link('Or Create account here...', ROUTES.SIGNUP)