from nicegui import ui

def Col(
    clas: str|None = "",
    props: str|None = "",
    styles: str|None = "",
    ):
    return ui.column().classes(clas).props(props).style(styles)

def Row(
    clas: str|None = "",
    props: str|None = "",
    styles: str|None = "",
    ):
    return ui.row().classes(clas).props(props).style(styles)

def Center(
    clas: str|None = "",
    props: str|None = "",
    styles: str|None = "",
    ):
    return ui.element().classes("flex justify-center items-center").classes(clas).props(props).style(styles)
