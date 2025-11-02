from UI import message, Raw, SoftBtn, Row, Col, TextArea, AddSpace, Notify, Label
from UI.Basic import Card, Header
from backend.Controllers import ControlChat
from library.formHandler import Variable
from utils.Storage import getUserStorage
from nicegui.ui import element
from nicegui.ui import run_javascript, menu, timer, scroll_area, context_menu, fab
from datetime import datetime
import json

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
        with fab("plus"):
            SoftBtn(
                icon="add_reaction",
                on_click=lambda:(), 
                rounded='full',
                px=1,
                py=1,
                clr='secondary',
                text_clr='primary',
                clas="flex h-10 aspect-square shadow-none border border-[var(--q-accent)]",
                icon_config={"size":"sm"}
            )
        SoftBtn(
            icon="send",
            on_click=on_send, 
            rounded='sm',
            clas="flex h-10 aspect-square shadow-none"
        )
    return r

async def copy_to_clipboard(content):
    await run_javascript(f"navigator.clipboard.writeText({json.dumps(content)})")
    Notify("Copied", color='success', icon='check')

async def delete(msg, r):
    response = await ControlChat.delete({'id': msg.get("id")})
    if response.get("success"):
        r.delete()
        Notify("Deleted successfully!", color="success")
    else:
        Notify("Cannot delete the message", color="error")

def addMessage(msg: dict, container: scroll_area, prev_msg: dict|None = None, index: int|None = None):
    seen = msg.get("seen_at", "")
    if isinstance(seen, datetime):
        dt1 = seen
    elif isinstance(seen, (int, float)):
        dt1 = datetime.fromtimestamp(seen)
    elif isinstance(seen, str) and seen.strip():
        dt1 = datetime.fromisoformat(seen)
    else:
        dt1 = datetime.now()
    readable = dt1.strftime("%b %d, %Y, %I:%M %p")
    def divider(content = "", classes = ""):
        with Row("w-full h-fit " + classes) as r:
            Label(content, "w-full text-center text-label")
        r.move(container)
    if prev_msg:
        dt2 = prev_msg.get("seen_at", "")
        if isinstance(seen, datetime):
            dt2 = dt2
        elif isinstance(dt2, (int, float)):
            dt2 = datetime.fromtimestamp(dt2)
        elif isinstance(dt2, str) and dt2.strip():
            dt2 = datetime.fromisoformat(dt2)
        else:
            dt2 = datetime.now()
        readable2 = dt2.strftime("%b %d, %Y, %I:%M %p")
        dt1parts = readable.split(",")
        dt2parts = readable2.split(',')
        daymon1, year1, time1 = dt1parts
        daymon2, year2, time2 = dt2parts
        if not year1.lower().strip() == year2.lower().strip():
            divider(readable.split(',')[1], "bg-secondary border border-[var(--q-primary)] bg-secodnary rounded-sm text-lg")
        if not daymon1.split(' ')[0].lower().strip() == daymon2.split(' ')[0].lower().strip():
            divider(readable.split(',')[0].split(' ')[0], "text-xs")
    elif index.__str__(): # So that 0 is also considered true
        if index == 0:
            divider(readable.split(',')[1], "bg-secondary border border-[var(--q-primary)] bg-secodnary rounded-sm")
            divider(readable.split(',')[0].split(' ')[0], "text-xs")
    with Row(clas="w-full h-fit items-center p-0 m-0 gap-0") as r:
        sent = msg.get("from_id") == getUserId()
        time = readable.split(",")
        date = time[0].split(' ')[1]
        time = time[2]
        if sent: AddSpace()
        print(sent)
        with Card().classes(
            f"max-w-[100%] md:max-w-[70%] p-2 rounded-xl shadow-sm text-label "
            f"{' bg-gradient-to-br from-[var(--q-accent)] to-[var(--q-secondary)] ' if sent else ' bg-white '} "
            f" transition-all duration-300 ease-in-out "
        ).style("cursor: pointer;") as msg_elem:
            with Col().classes("gap-0"):
                Raw.Html(msg.get("content", ""))
                Label(date + ', ' + time).classes("text-xs text-gray-500 text-right mt-1 italic")
            with context_menu().props("touch-position").classes("rounded-full") as c:
                async def copy(): 
                    await copy_to_clipboard(msg.get("content", ""))
                    c.close()
                async def dele():
                    await delete(msg, r)
                    c.close()
                with Raw.RawRow("w-full p-1 gap-1"):
                    SoftBtn(icon='content_copy',
                            rounded='full', px=1, py=1, 
                            on_click=copy
                            ).tooltip("Copy")
                    if sent:
                        SoftBtn(icon='delete', 
                                rounded='full', px=1, py=1,
                                on_click=dele,
                                clr="error"
                                ).tooltip("Delete")
                        SoftBtn(icon='edit', 
                                rounded='full', px=1, py=1, 
                                on_click=c.close
                                ).tooltip("Edit")
        if not sent: AddSpace()
    r.move(container)
    container.update()
    container.scroll_to(percent=100)

def addPreviousMessages(prev_chat, chat_messages, contianer):
    chat_messages.value = prev_chat.get("data", [])
    for page in (chat_messages.value or []):
        for i, msg in enumerate(page):
            if i>1: prev_msg = page[i-1]
            else: prev_msg = None
            addMessage(msg, contianer, prev_msg, i)

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

    # --- HEADER ---
    with header:
        SoftBtn(
            on_click=drawer.toggle,
            icon='menu',
            py=1, px=1
        )
        Label(
            user_data.get("name", "UnKnown"), 
            "text-text-primary text-xl font-bold truncate capitalize"
        )

    # --- BODY / CHAT AREA ---
    with container.classes("flex flex-col w-full h-[83vh] space-x-0 space-y-0 p-0 m-0"):
        chat_messages = Variable("chat_messages", [])
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
    c.move(footer)
    # --- RECEIVER (Timer) ---
    async def receiver_task():
        await receiveMessage(messages_col, chat_messages, user_data)
    timer(2.0, receiver_task)
