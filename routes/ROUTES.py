from functools import wraps
from utils.Auth import isAuthenticated
from utils import navigate

MAIN = '/'
LOGIN = '/login'
SIGNUP = '/signup'

def require_auth(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if isAuthenticated():
            return await func(*args, **kwargs)
        else:
            navigate(LOGIN)
    return wrapper
