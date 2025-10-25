from library.dbQuery import Query
from db.db import RUN_SQL
from library.validations import IsValidEmail, IsValidName, StrengthOfPswd
from backend.Models.ModelAuth import Auth
from bcrypt import checkpw
TABLE = "users"

async def _is_unique(value: str, column: str):
    query = Query(TABLE).select("COUNT(*)").where(**{column: value}).SQL()
    result = await RUN_SQL(query, to_fetch=True)
    count = result[0].get("COUNT(*)") if result else 0
    return count == 0

async def _validate(values: dict, can_be_empty=True) -> dict:
    name = values.get("name")
    email = values.get("email")
    pswd = values.get("password")
    conf = values.get("confirm")
    if name and can_be_empty: name = name.strip()
    if email and can_be_empty: email = email.strip()
    if pswd and can_be_empty: pswd = pswd.strip()
    if conf and can_be_empty: conf = conf.strip()
    errors = {}
    if name:
        if not IsValidName(name):
            errors['name'] = 'Name is invalid.'
        elif not await _is_unique(name, 'name'):
            errors['name'] = 'Name is already taken!'
    else:
        errors['name'] = 'Name is required!'
    if email:
        if not IsValidEmail(email):
            errors['email'] = 'Email is invalid.'
        elif not await _is_unique(email, 'email'):
            errors['email'] = 'Email is already taken!'
    else:
        errors['email'] = 'Email is required!'
    if not pswd:
        errors['password'] = 'Password is required.'
    elif StrengthOfPswd(pswd or '') < 4:
        errors['password'] = 'Password is weak!'
    elif not conf:
        errors['password'] = 'Confirm password is required.'
    elif not (pswd == conf):
        errors['password'] = 'Passwords do not match!'
    return errors

async def create(data: dict) -> dict:
    errors = await _validate(data)
    result = []
    if not errors:
        try:
            result = await Auth().create(data)
            if not isinstance(result, (list, tuple)):
                result = [result]
        except Exception as e:
            result = []
            errors['unknown'] = "Sorry, we cannot create your account!"
    success = not bool(errors)
    return {
        "success": success,
        "errors": errors,
        "data": result
    }

async def create(data: dict) -> dict:
    errors = await _validate(data)
    result = []
    if not errors:
        try:
            result = await Auth().create(data)
            if not isinstance(result, (list, tuple)):
                result = [result]
        except Exception as e:
            result = []
            errors['Unknown'] = "Sorry, we cannot create your account!"
    success = not bool(errors)
    return {
        "success": success,
        "errors": errors,
        "data": result
    }

async def login(data: dict) -> dict:
    identifier = data.get("identifier")
    password = data.get("password")
    errors = {}
    if not identifier: errors['identifier'] = "Email or Name is required!"
    if not password: errors['password'] = "Password is required!"
    user_data = {}
    if not errors:
        users = await Auth().getUserByIdentifier(identifier)
        if users and len(users) > 0:
            user_data = users[0]
            hashed_pw = user_data.get("password")
            if not checkpw(password.encode(), hashed_pw.encode()):
                errors['password'] = "Password is incorrect!"
                user_data = None
        else: errors['unknown'] = "Account not found!"
    success = not errors
    return {
        "success": success,
        "errors": errors,
        "data": user_data,
    }
