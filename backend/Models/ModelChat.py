from typing import Literal
from .Model import Model
from EXCEPTIONS import InvalidChoice, Required, NotFound, ValidationError
from library.dbQuery import Query
from db.db import RUN_SQL
import datetime

TABLE = "chat"
ALLOWED_STATUS = ('seen', 'sent', 'pending', 'error')

class Chat(Model):
    def __init__(self):
        super().__init__()

    # ----------------- CREATE -----------------
    async def _create(self, obj: dict):
        from_id = obj.get("from_id")
        to_id = obj.get("to_id")
        content = obj.get("content")
        reply_to_id = obj.get("reply_to_id")
        status = obj.get("status", "pending")

        if not from_id:
            raise Required("from_id")
        if not to_id:
            raise Required("to_id")
        if not content:
            raise Required("content")
        if status not in ALLOWED_STATUS:
            raise InvalidChoice(f"status must be one of {ALLOWED_STATUS}")

        SQL = Query(TABLE).insert(
            from_id=from_id,
            to_id=to_id,
            content=content,
            reply_to_id=reply_to_id,
            status=status,
            sent_at=datetime.datetime.utcnow()
        ).SQL()

        await RUN_SQL(SQL)
        FETCH = Query(TABLE).select().where(from_id=from_id, to_id=to_id).order_by("id DESC").limit(1).SQL()
        return await RUN_SQL(FETCH, True)

    # ----------------- UPDATE -----------------
    async def _update(self, obj: dict):
        message_id = obj.get("id")
        if not message_id:
            raise Required("Message ID")

        # Fetch current message
        current = await self.getMessageByID(message_id)
        if not current:
            raise NotFound(f"Message with id={message_id} not found.")

        allowed_fields = ["from_id", "to_id", "content", "reply_to_id", "status", "seen_at", "sent_at"]
        update_data = {k: v for k, v in obj.items() if k in allowed_fields}

        if "status" in update_data and update_data["status"] not in ALLOWED_STATUS:
            raise InvalidChoice(f"status must be one of {ALLOWED_STATUS}")

        if not update_data:
            raise ValidationError("No valid fields provided to update.")

        SQL = Query(TABLE).update(**update_data).where(id=message_id).SQL()
        await RUN_SQL(SQL)
        FETCH = Query(TABLE).select().where(id=message_id).SQL()
        return await RUN_SQL(FETCH, True)

    # ----------------- DELETE -----------------
    async def _delete(self, obj: dict):
        message_id = obj.get("id")
        if not message_id:
            raise Required("Message ID")

        message = await self.getMessageByID(message_id)
        if not message:
            raise NotFound(f"Message with id={message_id} not found.")

        SQL = Query(TABLE).delete().where(id=message_id).SQL()
        await RUN_SQL(SQL)
        return {"deleted": True}

    # ----------------- ROUTING -----------------
    async def _implement(self, mode: Literal['c', 'u', 'd'] = 'c', o: dict = {}):
        match mode:
            case 'c': return await self._create(o)
            case 'u': return await self._update(o)
            case 'd': return await self._delete(o)
            case _: raise InvalidChoice("Mode can only be 'c', 'u', or 'd'.")

    # ----------------- UTILITY METHODS -----------------
    async def getMessageByID(self, message_id: int|None):
        SQL = Query(TABLE).select().where(id=message_id).SQL()
        FETCH = await RUN_SQL(SQL, to_fetch=True)
        return FETCH

    async def getMessagesByUserID(self, user_id: int|None):
        SQL = Query(TABLE).select().where(from_id=user_id).orWhere(to_id=user_id).order_by("sent_at ASC").SQL()
        FETCH = await RUN_SQL(SQL, to_fetch=True)
        return FETCH

    async def getMessagesByToID(self, to_id: int|None):
        SQL = Query(TABLE).select().where(to_id=to_id).order_by("sent_at ASC").SQL()
        FETCH = await RUN_SQL(SQL, to_fetch=True)
        return FETCH

    async def getMessagesByFromID(self, from_id: int|None):
        SQL = Query(TABLE).select().where(from_id=from_id).order_by("sent_at ASC").SQL()
        FETCH = await RUN_SQL(SQL, to_fetch=True)
        return FETCH

    async def searchMessagesInContent(self, keyword: str):
        SQL = Query(TABLE).select().where(content__like=f"%{keyword}%").order_by("sent_at ASC").SQL()
        FETCH = await RUN_SQL(SQL, to_fetch=True)
        return FETCH

    async def getFullChat(self, from_id: int|None, to_id: int|None, page_size: int|None = 20):
        if from_id is None:
            raise Required("from_id")
        if to_id is None:
            raise Required("to_id")
        SQL = Query(TABLE).select().where(
            from_id=from_id, to_id=to_id
        ).orWhere(
            from_id=to_id, to_id=from_id
        ).order_by("sent_at ASC").SQL()
        messages = await RUN_SQL(SQL, to_fetch=True)
        if page_size:
            pages = [messages[i:i+page_size] for i in range(0, len(messages), page_size)]
            return pages
        return messages

    async def markAsSeen(self, message_id: int|None|None):
        if not message_id:
            raise Required("Message ID")
        message = await self.getMessageByID(message_id)
        if not message:
            raise NotFound(f"Message with id={message_id} not found.")
        SQL = Query(TABLE).update(
            status='seen',
            seen_at=datetime.datetime.utcnow()
        ).where(id=message_id).SQL()
        await RUN_SQL(SQL)
        FETCH = Query(TABLE).select().where(id=message_id).SQL()
        return await RUN_SQL(FETCH, True)

    # ----------------- PUBLIC INTERFACE -----------------
    async def implement(self, mode: Literal['c', 'u', 'd'], obj: dict | list = {}):
        result = []
        if isinstance(obj, (list, tuple)):
            for o in obj:
                if not isinstance(o, dict):
                    raise TypeError("Each item must be a dictionary with required keys.")
                result_o = await self._implement(mode, o)
                if result_o:
                    result.append(result_o)
        elif isinstance(obj, dict):
            result = await self._implement(mode, obj)
        else:
            raise TypeError(f"Object must be dict, list, or tuple — not {type(obj).__name__}.")
        return result

    async def create(self, obj): return await self.implement('c', obj)
    async def update(self, obj): return await self.implement('u', obj)
    async def delete(self, obj): return await self.implement('d', obj)
