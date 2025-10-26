from UI import Label
from ENV import APP_NAME, FAVICON

def CompHeaderTitle():
    return Label(APP_NAME + FAVICON, "text-2xl font-bold bg-secondary p-2 shadow-md rounded-md")