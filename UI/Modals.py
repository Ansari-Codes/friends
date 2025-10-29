from typing import Callable
from nicegui import ui
from UI.Basic import RawLabel, RawRow, SoftBtn, Icon, AddSpace

def Notify(message:str = '', **kwargs):
    ui.notify(message, position='top-right', close_button='❌', **kwargs)

def DialogHeader(
        title: str = "",
        close_icon: str|bool = True,
        close_text: str = "",
        on_close: Callable|None = None,
        close_config: dict|None = None,
    ):
    close_config = close_config or {}
    icon_to_show = None
    if isinstance(close_icon, str):
        icon_to_show = close_icon.strip() if close_icon.strip() else ""
    else:
        icon_to_show = "close" * close_icon
    with RawRow("w-full bg-secondary dark:bg-primary justify-between p-2 items-center justify-between gap-2") as header_:
        title_ = RawLabel(title, "text-2xl font-medium text-white")
        close_btn_ = None
        if (close_icon or close_text):
            close_btn_ = SoftBtn(
                close_text,
                on_click=on_close or (lambda:()),
                icon=icon_to_show,
                rounded='sm' if (not icon_to_show) and (close_text) else "full",
                clr='error',
                clas=f"border-2 border-red-300 shadow-none",
                px=1,
                py=1,
                **close_config
            )
    return header_

# def Dialog(
#         dialog: ui.dialog|None = None,
#         content: ui.element|None = None,
#         *,
#         title: str = "",
#         title_config: dict|None = None,
#         close: dict|None = None,
#         okay: dict|None = None,
#         cancel: dict|None = None,
#         persistent: bool = False,
#         header: bool|str = True,
#         footer: bool|str = True,
#     ):
#     dialog = dialog or ui.dialog()
#     if not title_config: title_config = {}
#     dialog.props('persistent'*persistent)
#     dialog.props('transition-show="flip-down" ')
    
#     with RawRow(
#         header if isinstance(header, str) 
#         else "w-full h-fit justify-between items-center"
#     ) as header_:
#         if title.strip(): RawLabel(title, **title_config)
#         if close:
#             SoftBtn(
#                 icon=close.get("icon", "close"),
#                 clas=close.get("clas", "rounded-full border-2 bg-error text-white"),
#                 props=close.get("props", ""),
#                 styles=close.get("style", ""),
#                 on_click=close.get("on_click", dialog.delete),
#                 **close.get("config", {})
#             )

#     with RawRow(
#         footer if isinstance(footer, str) 
#         else "w-full h-fit items-center"
#     ) as footer_:
#         AddSpace()
#         if okay:
#             SoftBtn(
#                 text=okay.get("text", "Okay"),
#                 icon=okay.get("icon", ""),
#                 clas=okay.get("clas", "rounded-sm bg-success text-white"),
#                 props=okay.get("props", ""),
#                 styles=okay.get("style", ""),
#                 on_click=okay.get("on_click", dialog.delete),
#                 **okay.get("config", {})
#             )
#         if cancel:
#             SoftBtn(
#                 text=cancel.get("text", "Cancel"),
#                 icon=cancel.get("icon", ""),
#                 clas=cancel.get("clas", "rounded-sm bg-error text-white"),
#                 props=cancel.get("props", ""),
#                 styles=cancel.get("style", ""),
#                 on_click=cancel.get("on_click", dialog.delete),
#                 **cancel.get("config", {})
#             )
#     if header: header_.move(dialog, 0)
#     return dialog, footer_
