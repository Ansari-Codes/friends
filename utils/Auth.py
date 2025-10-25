from nicegui import app


def isAuthenticated():
    return app.storage.user.get("auth", False)

def updateUserStorage(data):
    app.storage.user.update(data)
