from UI import message, Raw, SoftBtn, Button, Input, AddSpace
from backend.Controllers import ControlChat

def createMessageBox():
    with Input("w-full"):
        AddSpace(); Button(props='unelevated icon="send"')

def CompChat(to: dict|None = None):
    createMessageBox()
