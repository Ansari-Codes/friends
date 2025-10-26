from UI import message, Raw, SoftBtn, Button, RawButton, Input, Row, TextArea
from backend.Controllers import ControlChat
from library.formHandler import Variable

def createMessageBox(model=None, on_send = lambda :()):
    with Raw.RawRow("w-full items-end justify-center gap-1"):
        TextArea(
            "TextArea",
            max_h = '300px',
            min_h = '35px',
            overflow = 'y-auto',
            flexible = True,
            model = model,
            autogrow=True
        )
        SoftBtn(icon="send", on_click=on_send, clas="flex h-10 aspect-square shadow-none")

def CompChat(to: dict|None = None):
    message_content = Variable("message_content", "")
    createMessageBox(message_content, lambda : print(message_content.value))
