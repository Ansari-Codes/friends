from UI import Label, SoftBtn, Header, RawRow
from ENV import APP_NAME
from utils.Auth import isAuthenticated
from routes.ROUTES import LOGIN, SIGNUP, MAIN
from .CompHeaderTitle import CompHeaderTitle

def CompHeader():
    with Header(clas="flex flex-row justify-between items-center") as header:
        CompHeaderTitle()
        with RawRow(clas="w-fit gap-2"):
            if isAuthenticated():
                SoftBtn('Dashboard', link=MAIN)
            else:
                SoftBtn('Login', link=LOGIN)
                SoftBtn('Signup', link=SIGNUP)
    return header