from nicegui import app
from db.db import RUN_SQL
from library.dbQuery import Query

async def isAuthenticated() -> bool:
    user_id = app.storage.user.get("id")
    if app.storage.user.get("auth") and user_id is not None:
        sql = Query("users").select("id").where(id=user_id).limit(1).SQL()
        result = await RUN_SQL(sql, to_fetch=True)
        if not result:
            updateUserStorage({"auth": False})
            return False
        return True
    return False

def updateUserStorage(data):
    app.storage.user.update(data)
