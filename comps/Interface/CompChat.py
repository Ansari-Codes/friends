from UI import message, Raw, SoftBtn, Row, Col, TextArea, AddSpace, Notify
from backend.Controllers import ControlChat
from library.formHandler import Variable
from utils.Storage import getUserStorage

def getUserId(): return getUserStorage().get("id")
async def _fetch_chat(to: dict):
    return await ControlChat.getFullChat({
        "from_id": getUserId(),
        "to_id": to.get("id")
    })

async def send(model, chat, col, to: dict|None = None):
    to = to or {}
    msg = str(model.value or "").strip()
    if not msg:
        Notify("I need a message to send!", color="warning", icon="warning")
        return
    response = await ControlChat.send({
        "from_id": getUserId(),
        "to_id": to.get("id"),
        "content": msg
    })
    print(response)
    if response.get("success"):
        chat.value.append(response.get("data"))
    else:
        Notify("We cannot send your message!", color="error", icon="error")
        print(response.get("errors"))
        return
    with Row( clas="w-full") as r:
        AddSpace()
        msg_elem = message(text=msg, sent=True)
    r.move(col)
    model.value = ""

async def receive(messages, col):
    pass

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

async def CompChat(to: dict|None):
    to = to or {}
    to = await to.get("user", {})
    prev_chat = await _fetch_chat(to)
    if not prev_chat.get("success"): return

    chat_messages = Variable("chat_messages", prev_chat.get("data", []))
    message_content = Variable("message_content", "")

    # Parent container - full height
    with Raw.RawCol(clas="w-full h-full flex flex-col") as parent:

        # Chat messages area - 80% height, scrollable
        with Col(clas="w-full h-[80%] overflow-y-auto gap-2 p-2 bg-secondary") as messages_col:
            for page in (chat_messages.value or []):
                for msg in page:
                    sent = msg.get("from_id") == getUserId()
                    with Row(clas="w-full items-center"):
                        if sent: AddSpace()
                        message(text=msg.get("content"), sent=sent)
                        if not sent: AddSpace()

        # Message input area - 20% height
        with Col(clas="w-full h-[20%] p-2 bg-primary flex items-end"):
            createMessageBox(
                message_content,
                lambda col=messages_col: send(message_content, chat_messages, col, to)
            )
