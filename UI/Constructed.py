from nicegui import ui
from . import Raw, Basic

def LabeledInput(
        labels: dict|None  = None, 
        inputs: dict|None = None,
        clas: str|None = "",
        props: str|None = "", 
        styles: str|None = "",
        clas_lbl: str|None = "items-center justify-between gap-2",
        props_lbl: str|None = "", 
        styles_lbl: str|None = "", 
    ):
    labels = labels or {}
    inputs = inputs or {}
    group  = {
        "cont": None,
        "labels": {},
        "inputs": {},
        "errors": {},
    }
    with Raw.RawCol() as cont:
        for name, label in labels.items():
            with Raw.RawCol(clas=clas_lbl, props=props_lbl, styles=styles_lbl):
                group['labels'][name] = Raw.RawLabel(**{k:v for k,v in label.items() if k!='err'})
                group['errors'][name] = Raw.RawLabel(clas="text-red-500", source=label.get("err"))
        for name, inpu in inputs.items():
            group['inputs'][name] = Basic.Input(**inpu).classes("w-full")
    group["cont"] = cont
    cont.classes("w-full")
    cont.classes(clas).props(props).style(styles)
    return group
