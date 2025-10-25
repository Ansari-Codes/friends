from UI import SoftBtn, Button, INIT_THEME
from utils.Storage import clearUserStorage
from utils import navigate

async def create():
    INIT_THEME()
    SoftBtn("LogOut", on_click=lambda: [clearUserStorage(), navigate('/')])
    SoftBtn("Test", on_click=lambda: print("Testing"))
    Button("Test")
