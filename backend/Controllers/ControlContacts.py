from backend.Models.ModelAuth import Auth
from backend.Models.ModelChat import Chat

auth = Auth()
chat = Chat()

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

        # --- Group messages by contact_id ---
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

        # --- Fetch user data for each contact ---
        for contact_id in contacts_dict.keys():
            user_info = await auth.getUserById(contact_id)
            if user_info:
                user_data = user_info[0]
                user_data.pop("password", None)
                contacts_dict[contact_id]["user"] = user_data

        # --- Convert dict to list ---
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
