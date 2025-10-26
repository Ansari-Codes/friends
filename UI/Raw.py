from typing import Any
from nicegui import ui

def Html(
        content: str = "",
        clas: str|None = "",
        props: str|None = "",
        styles: str|None = "",
    ):
    return ui.html(content, sanitize=lambda x: x).classes(clas).props(props).style(styles)

def Div(       
        clas: str|None = "", 
        props: str|None = "",
        styles: str|None = "",
    ):
    return ui.element().classes(clas).props(props).style(styles)

def RawButton(
        content: str|Any = "",
        on_click = lambda: (),
        clas: str|None = "", 
        props: str|None = "",
        styles: str|None = "",
    ):
    elem = ui.html(content, sanitize=lambda c: c, tag='button'
        ).on('click', on_click
        ).classes(clas
        ).style(styles
        ).props(props)
    return elem

def RawRow(
        clas: str|None = "", 
        props: str|None = "",
        styles: str|None = "",
    ):
    return ui.element().classes("flex flex-row").classes(clas).props(props).style(styles)

def RawCol(
        clas: str|None = "", 
        props: str|None = "",
        styles: str|None = "",
    ):
    return ui.element().classes("flex flex-row").classes(clas).props(props).style(styles)

def RawLabel(
        text: str = "",
        clas: str|None = "", 
        props: str|None = "",
        styles: str|None = "",
        source: Any = None
    ):
    html = ui.html(
            text or "",
            sanitize=lambda c: c, 
            tag='p'
        ).classes(clas).props(props).style(styles)
    if source:
        assert hasattr(source, 'value'), "Given source object should have value attribute"
        html.content = source.value or ""
        html.bind_content_from(source, 'value')
    return html