import asyncio
from UI import message, Raw, SoftBtn, Row, Col, TextArea, AddSpace, Notify, Label
from UI.Basic import Header
from backend.Controllers import ControlChat
from library.formHandler import Variable
from utils.Storage import getUserStorage
from nicegui.ui import element
from ENV import THEME_DEFAULT
from nicegui.ui import run_javascript, timer, context, scroll_area

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
        msg = response.get("data", [])[0]
        addMessage(msg, col)
    else:
        Notify("We cannot send your message!", color="error", icon="error")
        print(response.get("errors"))

def createMessageBox(model=None, on_send=lambda:()):
    with Raw.RawRow("") as r:
        TextArea(
            "TextArea",
            max_h='120px',
            min_h='35px',
            overflow='y-auto',
            flexible=True,
            model=model,
            autogrow=True,
            clas="bg-inp rounded-sm",
            config=dict(
                placeholder = "Your Message Here...",
            )
        )
        SoftBtn(
            icon="send",
            on_click=on_send, 
            rounded='sm',
            clas="flex h-10 aspect-square shadow-none"
        )
    return r

def addMessage(msg: dict, container: scroll_area):
    with Row(clas="w-full h-fit items-center p-0 m-0 gap-0") as r:
        sent = msg.get("from_id") == getUserId()
        if sent: 
            AddSpace()
        msg_elem = message(text=msg.get("content"), sent=sent)
        msg_elem.classes("max-w-[80%] sm:max-w-[60%]")
        if not sent:
            AddSpace()
    r.move(container)
    container.update()
    container.scroll_to(percent=100, duration=0.2)

def addPreviousMessages(prev_chat, chat_messages, contianer):
    chat_messages.value = prev_chat.get("data", [])
    for page in (chat_messages.value or []):
        for msg in page:
            addMessage(msg, contianer)

async def receiveMessage(container: scroll_area, chat: Variable, to: dict|None = None):
    to = to or {}
    response = await ControlChat.receive({
        "from_id": to.get("id"),
        "to_id": getUserId(),
    })
    if response.get("success"):
        msg = response.get("data", {})
        if not msg or not msg.get("id"):  # Check if message is valid
            return
            
        # Check if message already exists using message ID instead of timestamp
        msg_id = msg.get("id")
        is_duplicate = False
        for page in (chat.value or []):
            if any(m.get("id") == msg_id for m in page):
                is_duplicate = True
                break
                
        if is_duplicate:
            return
            
        # Add message to chat variable
        if not chat.value:
            chat.value = [[]]
        if not chat.value[-1]:  # If last page is empty
            chat.value[-1].append(msg)
        elif len(chat.value[-1]) >= 20:  # If last page is full, create new page
            chat.value.append([msg])
        else:  # Add to last page
            chat.value[-1].append(msg)
            
        # Add message to UI
        addMessage(msg, container)
        container.update()

async def CompChat(to: dict | None, container: element, drawer, header, footer):
    to = to or {}
    user_data = to.get("user", {})
    if not user_data or not user_data.get("id"):
        Notify("Invalid contact selected", color='red', icon='error')
        return

    # Reset layout
    container.clear()
    header.clear()
    footer.clear()
    header.set_visibility(True)
    footer.set_visibility(True)

    # Lock layout viewport
    page_layout = context.client.layout
    page_layout.props(remove='view', add='view="lHh lpR lFf"')

    # --- HEADER ---
    with header.props("dense").classes("bg-primary text-white flex items-center h-[7vh] p-0 px-2 space-x-0 space-y-0"):
        SoftBtn(
            on_click=drawer.toggle,
            icon='menu',
            py=1, px=1
        )
        Label(
            user_data.get("name", "UnKnown"), 
            "text-white text-xl font-bold truncate capitalize"
        )

    # --- BODY / CHAT AREA ---
    with container.classes("flex flex-col w-full h-[83vh] space-x-0 space-y-0 p-0 m-0"):
        chat_messages = Variable("chat_messages", [])

        # ✅ this is the only scrollable section
        # messages_col = Raw.RawCol(
        #     "w-full flex-1 overflow-y-auto px-4 py-3 gap-2 items-end justify-end scroll-smooth"
        # )
        messages_col = scroll_area().classes("h-[81vh]")
        messages_col.props('id="chat-container"')

        prev_chat = await _fetch_chat(user_data)
        if prev_chat.get("success"):
            addPreviousMessages(prev_chat, chat_messages, messages_col)
        else:
            Label("Failed to load chat history", "text-red-400 text-center")

    # --- FOOTER / MESSAGE BOX ---
    message_content = Variable("message_content", "")
    c = createMessageBox(
        message_content,
        lambda: send(message_content, chat_messages, messages_col, user_data)
    )
    c.classes("w-full flex gap-2 items-end backdrop-blur-sm")
    c.props("dense")
    footer = footer.classes("bg-primary text-white flex items-center h-[7vh] p-0 px-2 space-x-0 space-y-0")
    footer = footer.props("dense")
    c.move(footer)

    # --- RECEIVER (Timer) ---
    import asyncio
    async def receiver_task():
        await receiveMessage(messages_col, chat_messages, user_data)
    timer(2.0, lambda: asyncio.create_task(receiver_task()))
