from UI import SoftBtn, Label, Button, INIT_THEME
from utils.Storage import clearUserStorage
from utils import navigate
from library.formHandler import Variable
from comps.Interface import CompChat

async def create():
    INIT_THEME()
    CompChat.CompChat()
    SoftBtn("LogOut", on_click=lambda: [clearUserStorage(), navigate('/')])