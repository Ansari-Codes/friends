from UI import message, Raw, SoftBtn, Row, Col, TextArea, AddSpace, Notify, Label
from backend.Controllers import ControlChat
from library.formHandler import Variable
from utils.Storage import getUserStorage
from nicegui.ui import element
from ENV import THEME_DEFAULT
from nicegui.ui import run_javascript

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

def createUserInfo(info: dict):
    with Raw.RawRow("") as r:
        Label(f"{info.get('name', '')} ({info.get('email', '')})",
            "text-white font-medium truncate px-2")
    return r

def createMessageBox(model=None, on_send=lambda:()):
    with Raw.RawRow("") as r:
        TextArea(
            "TextArea",
            max_h='120px',
            min_h='35px',
            overflow='y-auto',
            flexible=True,
            model=model,
            autogrow=False,
            clas="bg-inp rounded-sm",
            config=dict(
                placeholder = "Your Message Here..."
            )
        )
        SoftBtn(
            icon="send",
            on_click=on_send, 
            rounded='sm',
            clas="flex h-10 aspect-square shadow-none"
        )
    return r

def addPreviousMessages(prev_chat, chat_messages, contianer):
    chat_messages.value = prev_chat.get("data", [])
    for page in (chat_messages.value or []):
        for msg in page:
            sent = msg.get("from_id") == getUserId()
            with Row(clas="w-full h-fit items-center p-0 m-0 gap-0") as r:
                if sent: 
                    AddSpace()
                msg_elem = message(text=msg.get("content"), sent=sent)
                msg_elem.classes("max-w-[80%] sm:max-w-[60%]")
                if not sent:
                    AddSpace()
            r.move(contianer)

async def CompChat(to: dict | None, container: element):
    to = to or {}
    user_data = to.get("user", {})
    if not user_data or not user_data.get("id"):
        Notify("Invalid contact selected", color='red', icon='error')
        return
    container.clear()
    with container.classes("gap-1 w-full"):
        # User Info
        u = createUserInfo(user_data)
        u.classes("w-full h-[6vh] gap-1 items-center justify-center bg-primary rounded-xl")

        # Message Show
        chat_messages = Variable("chat_messages", [])
        messages_col = Raw.RawCol(
            f"w-full h-[82vh] items-end justify-end overflow-y-auto bg-secondary p-6 rounded-xl border border-[{THEME_DEFAULT.get('primary', '#2e712e')}]"
        )
        messages_col.props('id="chat-container"')
        prev_chat = await _fetch_chat(user_data)
        if prev_chat.get("success"):
            addPreviousMessages(prev_chat, chat_messages, messages_col)
        else: Label("Failed to load chat history")
        run_javascript("""
            const chatContainer = document.getElementById('chat-container');
            const observer = new MutationObserver(() => {
                chatContainer.scrollTop = chatContainer.scrollHeight;
            });
            observer.observe(chatContainer, { childList: true, subtree: true });
        """)
        # Message Box
        message_content = Variable("message_content", "")
        c = createMessageBox(
                message_content,
                lambda: send(message_content, chat_messages, messages_col, user_data)
            )
        c.classes("w-full h-[6vh] gap-1 items-center justify-center")
