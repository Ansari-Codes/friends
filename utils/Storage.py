from nicegui import app

def updateUserStorage(data: dict):
    app.storage.user.update(data)

def setUserStorage(data: dict):
    app.storage.user.clear()
    app.storage.user.update(data)

def clearUserStorage():
    app.storage.user.clear()

def getUserStorage():
    return dict(app.storage.user)
