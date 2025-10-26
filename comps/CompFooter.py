from UI import Label, RawLabel, Footer, RawRow, Link
from ENV import APP_NAME
from utils.Auth import isAuthenticated
from routes.ROUTES import LOGIN, SIGNUP

def CompFooter():
    with Footer(clas="flex flex-row justify-between items-center") as footer:
        RawLabel(APP_NAME + " &copy; 2025, All rights reserved!")
        with RawRow(clas="w-fit gap-1"):
            if not isAuthenticated():
                Link('Login', LOGIN, clas="text-white")
                RawLabel(".", clas="text-white")
                Link('Signup', SIGNUP, clas="text-white")
    return footer
