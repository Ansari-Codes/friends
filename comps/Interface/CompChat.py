from UI import message, Raw, SoftBtn, Button, RawButton, Input, Row, TextArea
from backend.Controllers import ControlChat
from library.formHandler import Variable
from utils.Storage import getUserStorage

def getUserId(): return getUserStorage().get("id")

async def _fetch_chat(to: dict):
    return await ControlChat.getFullChat({
        "from_id": getUserId(),
        "to_id": to.get("id"),
        "page_size": 100
    })

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

async def CompChat(to: dict|None = None):
    if not to: to={}
    prev_chat = await _fetch_chat(to)
    if not prev_chat.get("success"): return
    chat_messages = Variable("chat_messages", prev_chat.get("data"))
    message_content = Variable("message_content", "")
    createMessageBox(message_content, lambda : print(message_content.value))
