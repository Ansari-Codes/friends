from .Raw import *
from .Basic import *
from .Layouts import *
from nicegui.ui import spinner, linear_progress, circular_progress

def showLoading(text: str = "", text_config=None, spnr_config=None):
    text_config = text_config or {}
    spnr_config = spnr_config or {'size':'100px'}
    with RawCol().classes("w-full h-full justify-center items-center") as cont:
        if text:
            labl = Label(
                text, 
                **text_config
            )
        spnr = spinner(
        **{
            k:v for k,v in spnr_config.items() 
            if k not in ['clas', 'props', 'styles']
            }
        ).classes(spnr_config.get("clas")).props(spnr_config.get("props")).style(spnr_config.get("styles"))
    return cont

