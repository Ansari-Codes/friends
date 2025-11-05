from typing import Literal
from .Model import Model
from EXCEPTIONS import InvalidChoice, Required, NotFound, ValidationError
from library.dbQuery import Query
from db.db import RUN_SQL
from db.Migrations.MIGRATIONS import TABLE_USERS
import bcrypt

TABLE = TABLE_USERS

class Auth(Model):
    def __init__(self):
        super().__init__()

    # ----------------- CREATE -----------------
    async def _create(self, obj: dict):
        name = obj.get("name")
        email = obj.get("email")
        password = obj.get("password")

        if not name: raise Required("Name")
        if not email: raise Required("Email")
        if not password: raise Required("Password")
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        SQL = Query(TABLE).insert(
            name=name,
            email=email,
            password=hashed_password,
        ).SQL()

        response = await RUN_SQL(SQL)
        print(response)
        FETCH = Query(TABLE).select().where(name=name).SQL()
        ANS = await RUN_SQL(FETCH, True)
        print(ANS)
        return ANS

    # ----------------- UPDATE -----------------
    async def _update(self, obj: dict):
        id_ = obj.get("id")
        name = obj.get("name")
        email = obj.get("email")
        prevpswd = obj.get("prevpswd", "")
        new_password = obj.get("password", "")

        if not id_:
            raise Required("User ID")

        user = await self.getUserById(id_)
        if not user:
            raise NotFound(f"User with id={id_} not found.")

        stored_hash = user[0].get("password", "")

        # Verify old password only if new password is provided
        if new_password:
            if not prevpswd:
                raise Required("Previous Password is required as 'password' key.")
            if not bcrypt.checkpw(prevpswd.encode(), stored_hash.encode()):
                raise ValidationError("Previous password does not match.")
            hashed_new = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
        else:
            hashed_new = stored_hash  # keep existing

        SQL = Query(TABLE).update(
            name=name,
            email=email,
            password=hashed_new
        ).where(id=id_).SQL()

        await RUN_SQL(SQL)
        FETCH = Query(TABLE).select().where(id=id_).SQL()
        return await RUN_SQL(FETCH, True)

    # ----------------- DELETE -----------------
    async def _delete(self, obj: dict):
        id_ = obj.get("id")
        password = obj.get("password", "")

        if not id_:
            raise Required("User ID")
        if not password:
            raise Required("Password is required as 'password' key.")

        user = await self.getUserById(id_)
        if not user:
            raise NotFound(f"User with id={id_} not found.")

        stored_hash = user[0].get("password", "")
        if not bcrypt.checkpw(password.encode(), stored_hash.encode()):
            raise ValidationError("Password does not match.")

        SQL = Query(TABLE).delete().where(id=id_).SQL()
        await RUN_SQL(SQL)
        return {"deleted": True}

    # ----------------- ROUTING -----------------
    async def _implement(self, mode: Literal['c', 'u', 'd'] = 'c', o: dict = {}):
        match mode:
            case 'c': return await self._create(o)
            case 'u': return await self._update(o)
            case 'd': return await self._delete(o)
            case _: raise InvalidChoice("Mode can only be 'c', 'u', or 'd'.")

    async def getUserById(self, id_):
        SQL = Query(TABLE).select().where(id=id_).SQL()
        FETCH = await RUN_SQL(SQL, to_fetch=True)
        return FETCH
    
    async def getUserByIdentifier(self, entity: str):
        SQL = Query(TABLE).select().where(
                email = entity
            ).orWhere(name = entity).SQL()
        FETCH = await RUN_SQL(SQL, to_fetch=True)
        return FETCH

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
