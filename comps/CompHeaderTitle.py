from UI import Label, Link
from ENV import APP_NAME, FAVICON

def CompHeaderTitle(link: str|None = None):
    if link:
        return Link(
            APP_NAME + FAVICON, 
            str(link), 
            underline=False,
            clas=("text-2xl select-none font-bold bg-secondary p-2 shadow-md rounded-md no-underline text-white cursor-pointer hover:no-underline")
            )
    else:
        return Label(
            APP_NAME + FAVICON, 
            "text-2xl font-bold select-none bg-secondary p-2 shadow-md rounded-md"
            )
