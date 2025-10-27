from typing import Any, Callable, Literal
from nicegui import ui
from .Raw import RawRow, RawLabel
from nicegui.events import GenericEventArguments
from .Layouts import Row
from ENV import THEME_DEFAULT

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
        underline:  bool = True,
        new_tab: bool = False,
        clas: str|None = "", 
        props: str|None = "",
        styles: str|None = "",
    ):
    return ui.link(text, link, new_tab).classes(
        "hover:underline"*underline
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
        icon_config: dict|None = None,
        px: int = 4,
        py: int = 2,
        clr: str = "btn",
        ripple: bool = True,
        hover_effects: bool = True,
        active_effects: bool = True,
        text_align: Literal['left', 'center', 'right'] = 'center',
    ):
    colors = list(THEME_DEFAULT.keys())
    clr = clr or "transparent"
    if '/' in clr: c = clr.split('/')[0]
    else: c = clr
    if c not in colors+['transparent']: c = f"[{c}]"
    print(c)
    icon_config = icon_config or {}
    base_classes = (
        f"flex items-center justify-center gap-0 text-{text_align or 'center'} "
        f"px-{px} py-{py} rounded-sm text-white text-[14px] font-medium "
        f"transition-all duration-200 ease-in-out "
        f"bg-{c} shadow-md {'hover:shadow-lg'*bool(hover_effects)} {'active:scale-95'*bool(active_effects)} "
        f"select-none cursor-pointer {'ripple'*bool(ripple)} no-underline"
    )
    classes = f"{base_classes} {clas or ''}".strip()
    with (ui.link("", link, new_tab) if link else Row()).classes(classes).props(props).style(styles) as btn:
        if icon:
            ui.icon(icon, **icon_config).classes("text-[18px]")
        if text:
            ui.label(text)
    btn = btn.on('click', on_click)
    return btn

def Input(
        clas: str|None = "", 
        props: str|None = "",
        styles: str|None = "",
        model = None,
        default_props: bool|None = True,
        **kwargs
    ):
    inp = ui.input(
        **kwargs
    ).props(
        "dense outlined"*bool(default_props) + ' '+ (props or '')
    ).classes(clas).props(props).style(styles)
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

def TextArea(
        content: str = "",
        model=None,
        clas: str|None = "",
        props: str|None = "",
        styles: str|None = "",
        autogrow: bool = False,
        max_h: str|None = None,
        min_h: str|None = None,
        overflow: str|None = None,
        flexible: bool = False,
        config: dict|None = None
    ):
    if not config: config = {}
    ta = ui.input(value=content, **config)
    inner_classes = ""
    if model: ta.bind_value(model)
    if flexible: inner_classes += " flex-grow flex-shrink resize-none"
    if min_h: inner_classes += f" min-h-[{min_h}]"
    if max_h: inner_classes += f" max-h-[{max_h}]"
    if overflow: inner_classes += f" overflow-{overflow}"
    if autogrow: ta.props('autogrow')
    ta.classes(inner_classes)
    ta.classes(clas).props('dense outlined').props(props).style(styles)
    return ta

def AddSpace():
    return ui.space()

def Icon(
        name: str = "" , 
        size: str|None = None,
        color: str|None = None,
        clas: str|None = "", 
        props: str|None = "",
        styles: str|None = "",
    ):
    return ui.icon(name, size=size, color=color).classes(clas).props(props).style(styles)