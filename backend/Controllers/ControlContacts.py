from backend.Models.ModelAuth import Auth
from backend.Models.ModelChat import Chat
from db.db import RUN_SQL

auth = Auth()
chat = Chat()
USERS = 'users'

async def get_contacts(user_id: int | None):
    if not user_id:
        return {
            "success": False,
            "errors": {"user_id": "Not Given"},
            "data": []
        }
    try:
        all_messages = await chat.getMessagesByUserID(user_id)
        if not all_messages:
            return {
                "success": True,
                "errors": None,
                "data": []
            }
        contacts_dict = {}
        for msg in all_messages:
            from_id = msg.get("from_id")
            to_id = msg.get("to_id")
            contact_id = to_id if from_id == user_id else from_id
            if contact_id not in contacts_dict:
                contacts_dict[contact_id] = {
                    "user": None,
                    "messages": []
                }
            contacts_dict[contact_id]["messages"].append(msg)
        for contact_id in contacts_dict.keys():
            user_info = await auth.getUserById(contact_id)
            if user_info:
                user_data = user_info[0]
                user_data.pop("password", None)
                contacts_dict[contact_id]["user"] = user_data
        contacts_list = list(contacts_dict.values())
        return {
            "success": True,
            "errors": None,
            "data": contacts_list
        }
    except Exception as e:
        return {
            "success": False,
            "errors": {"exception": str(e)},
            "data": []
        }

async def get_All_users():
    
    try:
        all_users = await RUN_SQL(f"SELECT * FROM {USERS}", to_fetch=True)
        all_users = list(all_users)
        error = None
    except Exception as e:
        error = str(e)
        all_users = []
    return {
        "success": not error,
        "error": error,
        "data": all_users
    }