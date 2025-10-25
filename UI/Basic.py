from typing import Callable, Literal
from nicegui import ui
from .Raw import RawRow, RawLabel

def Label(
        text: str = "", 
        clas: str|None = "", 
        props: str|None = "",
        styles: str|None = "",
        config: dict|None = None
    ):
    if not config: config = {}
    return ui.label(text=text, **config).classes(clas).props(props).style(styles)

def Header(
        clas: str|None = "", 
        props: str|None = "",
        styles: str|None = "",
        config: dict|None = None
    ):
    if not config: config = {}
    return ui.header(**config).classes(clas).props(props).style(styles)

def Footer(
        clas: str|None = "", 
        props: str|None = "",
        styles: str|None = "",
        config: dict|None = None
    ):
    if not config: config = {}
    return ui.footer(**config).classes(clas).props(props).style(styles)

def Card(
        clas: str|None = "", 
        props: str|None = "",
        styles: str|None = "",
        align: Literal['start', 'end', 'center', 'baseline', 'stretch']|None = None
    ):
    return ui.card(align_items=align).classes(clas).props(props).style(styles)

def Link(
        text: str = "",
        link: str = "",
        new_tab: bool = False,
        clas: str|None = "", 
        props: str|None = "",
        styles: str|None = "",
    ):
    return ui.link(text, link, new_tab).classes(
        "hover:underline"
    ).classes(clas).props(props).style(styles)

def SoftBtn(
        text: str = "",
        on_click: Callable = lambda: (),
        link: str = "",
        new_tab: bool = False,
        icon: str = "",
        clas: str|None = "", 
        props: str|None = "",
        styles: str|None = "",
    ):
    base_classes = (
        "inline-flex items-center justify-center gap-2 "
        "px-4 py-2 rounded-sm text-white text-[14px] font-medium "
        "transition-all duration-200 ease-in-out "
        "bg-btn shadow-md hover:shadow-lg active:scale-95 "
        "select-none cursor-pointer ripple no-underline"
    )
    classes = f"{base_classes} {clas or ''}".strip()
    with (ui.link("", link, new_tab) if link else RawRow()).classes(classes).props(props).style(styles) as btn:
        if icon:
            ui.icon(icon).classes("text-[18px]")
        if text:
            ui.label(text)
    btn = btn.on('click', on_click)
    return btn

def Input(
        clas: str|None = "", 
        props: str|None = "",
        styles: str|None = "",
        model = None,
        **kwargs
    ):
    inp = ui.input(**kwargs).props("dense outlined").classes(clas).props(props).style(styles)
    if model:
        inp.bind_value(model, 'value')
    return inp

def Button(
        text: str = "", 
        on_click = lambda: (),
        clas: str|None = "", 
        props: str|None = "",
        styles: str|None = "",
        config: dict|None = None
    ):
    if not config: config = {}
    return ui.button(text=text, on_click=on_click, **config).classes(clas).props(props).style(styles)

def AddSpace():
    return ui.space()
