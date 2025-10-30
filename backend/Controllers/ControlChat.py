from library.dbQuery import Query
from db.db import RUN_SQL
from backend.Models.ModelChat import Chat
from EXCEPTIONS import Required, NotFound, ValidationError

TABLE = "chat"
USERS_TABLE = "users"
PAGE_SIZE = 20

# ------------------ VALIDATIONS ------------------
async def _exists_in_users(user_id: int) -> bool:
    if not user_id:
        return False
    query = Query(USERS_TABLE).select("COUNT(*)").where(id=user_id).SQL()
    result = await RUN_SQL(query, to_fetch=True)
    count = result[0].get("COUNT(*)", 0) if result else 0
    return count > 0

async def _exists_in_chat(message_id: int) -> bool:
    if not message_id:
        return False
    query = Query(TABLE).select("COUNT(*)").where(id=message_id).SQL()
    result = await RUN_SQL(query, to_fetch=True)
    count = result[0].get("COUNT(*)", 0) if result else 0
    return count > 0

async def _validate(data: dict) -> dict:
    errors = {}
    from_id = data.get("from_id")
    to_id = data.get("to_id")
    content = data.get("content")
    reply_to_id = data.get("reply_to_id")
    if not from_id:
        errors["from_id"] = "from_id is required."
    elif not await _exists_in_users(from_id):
        errors["from_id"] = f"User with id={from_id} does not exist."
    if not to_id:
        errors["to_id"] = "to_id is required."
    elif not await _exists_in_users(to_id):
        errors["to_id"] = f"User with id={to_id} does not exist."
    if not content:
        errors["content"] = "Content is required."
    if reply_to_id is not None and not await _exists_in_chat(reply_to_id):
        errors["reply_to_id"] = f"Reply message with id={reply_to_id} does not exist."
    return errors

# ------------------ CONTROLLER FUNCTIONS ------------------
async def send(data: dict) -> dict:
    errors = await _validate(data)
    result = []
    if not errors:
        try:
            result = await Chat().create(data)
            if not isinstance(result, (list, tuple)):
                result = [result]
        except Exception as e:
            errors["unknown"] = f"Message could not be sent! ({str(e)})"
            result = []
    return {"success": not bool(errors), "errors": errors, "data": result}

async def receive(data: dict) -> dict:
    from_id = data.get("from_id")
    to_id = data.get("to_id")
    errors = {}
    if not from_id:
        errors["from_id"] = "from_id is required."
    if not to_id:
        errors["to_id"] = "to_id is required."
    if not errors:
        pages = await Chat().getFullChat(from_id, to_id)
        last_message = None
        if pages and pages[-1]:  # Check if there are pages and the last page is not empty
            last_message = pages[-1][-1]  # Get the last message from the last page
        if last_message:
            message_id = last_message.get("id") #type:ignore
            await Chat().markAsSeen(message_id)
        return {"success": True, "errors": {}, "data": last_message}
    return {"success": False, "errors": errors, "data": None}

async def delete(data: dict) -> dict:
    message_id = data.get("id")
    errors = {}
    if not message_id:
        errors["id"] = "Message ID is required."
    elif not await _exists_in_chat(message_id):
        errors["id"] = f"Message with id={message_id} does not exist."
    if not errors:
        result = await Chat().delete({"id": message_id})
        return {"success": True, "errors": {}, "data": result}
    return {"success": False, "errors": errors, "data": None}

async def getFullChat(data: dict) -> dict:
    from_id = data.get("from_id")
    to_id = data.get("to_id")
    page_size = data.get("page_size", PAGE_SIZE)
    errors = {}
    if not from_id:
        errors["from_id"] = "from_id is required."
    if not to_id:
        errors["to_id"] = "to_id is required."
    if not errors:
        pages = await Chat().getFullChat(from_id, to_id, page_size)
        return {"success": True, "errors": {}, "data": pages}
    return {"success": False, "errors": errors, "data": []}
