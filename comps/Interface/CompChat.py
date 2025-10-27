from UI import message, Raw, SoftBtn, Row, Col, TextArea, AddSpace, Notify, Label
from backend.Controllers import ControlChat
from library.formHandler import Variable
from utils.Storage import getUserStorage
from nicegui.ui import element

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
    if response.get("success"):
        chat.value.append(response.get("data"))
        model.value = ""
        with Row(clas="w-full") as r:
            AddSpace()
            msg_elem = message(text=msg, sent=True)
        r.move(col)
    else:
        Notify("We cannot send your message!", color="error", icon="error")
        print(response.get("errors"))

def createMessageBox(model=None, on_send=lambda:()):
    with Raw.RawRow("w-full items-end justify-center gap-1"):
        TextArea(
            "TextArea",
            max_h='300px',
            min_h='35px',
            overflow='y-auto',
            flexible=True,
            model=model,
            autogrow=True
        )
        SoftBtn(icon="send", on_click=on_send, clas="flex h-10 aspect-square shadow-none")

def addPreviousMessages(prev_chat, chat_messages):
    chat_messages.value = prev_chat.get("data", [])
    for page in (chat_messages.value or []):
        for msg in page:
            sent = msg.get("from_id") == getUserId()
            with Row(clas="w-full items-center"):
                if sent: 
                    AddSpace()
                msg_elem = message(text=msg.get("content"), sent=sent)
                if not sent: 
                    AddSpace()
    
async def CompChat(to: dict|None, container: element):
    to = to or {}
    user_data = to.get("user", {})
    if not user_data or not user_data.get("id"):
        with container:
            Label("Invalid contact selected")
        return
    container.clear()
    chat_messages = Variable("chat_messages", [])
    with container:
        messages_col = Col(clas="w-full h-[80%] overflow-y-auto gap-2 p-2 bg-secondary")
        prev_chat = await _fetch_chat(user_data)
        if prev_chat.get("success"): addPreviousMessages(prev_chat, chat_messages)
        else: Label("Failed to load chat history")
        with Col(clas="w-full h-[20%] p-2 bg-primary flex items-end"):
            message_content = Variable("message_content", "")
            createMessageBox(
                message_content,
                lambda: send(message_content, chat_messages, messages_col, user_data)
            )