from typing import Callable
from nicegui import ui
from UI.Basic import RawLabel, RawRow, SoftBtn, Icon

def Notify(message:str = '', **kwargs):
    ui.notify(message, position='bottom-left', **kwargs)

def ShowDialog(
        dialog: ui.dialog|None,
        *,
        title: str = "",
        title_config: dict|None = None,
        close: dict|None = None,
        okay: dict|None = None,
        cancel: dict|None = None,
        persistent: bool = False,
        header: bool|str = True
    ):
    dialog = ui.dialog()
    if not title_config: title_config = {}
    if not close: close = {}
    with RawRow(
        header if isinstance(header, str) 
        else "w-full h-fit justify-between items-center") as close_row:
        if title.strip(): RawLabel(title, **title_config)
        if close:
            SoftBtn(
                icon=close.get("icon", "close"),
                clas=close.get("clas", "rounded-full border-2 bg-error text-white"),
                props=close.get("props", ""),
                styles=close.get("style", ""),
                on_click=close.get("on_click", lambda d=dialog: d.delete()),
                **close.get("config", {})
            )
    if header:
        close_row.move(dialog, 0)
