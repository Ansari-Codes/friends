from UI import Label, SoftBtn, Input, INIT_THEME, Div, Select
from nicegui.ui import colors, query
from nicegui import app
from utils.Storage import getUserStorage, updateUserStorage
from ENV import BASIC

PRESETS = {
    "Default": BASIC,
    "Dark": {
        'name': 'Dark',
        'primary' : "#024125",
        'secondary' : "#284e35",
        'accent' : "#001905",
        'btn' : "#2F492E",
        'inp' : "#477046",
        'success' : '#21ba45',
        'error' : '#c10015',
        'info' : '#31ccec',
        'warning' : '#f2c037',
        'text-primary': "#ffffff",
        'text-secondary': "#d3d3d3",
        'label': "#b3b1b1"
    },
    "Light": {
        'name': 'Light',
        'primary' : "#639B61",
        'secondary' : "#bff8c3",
        'accent' : "#FFFFFF",
        'btn' : "#78C475",
        'inp' : "#F9F9F9",
        'success' : '#21ba45',
        'error' : '#c10015',
        'info' : '#31ccec',
        'warning' : '#f2c037',
        'text-primary': "#000000",
        'text-secondary': "#294227",
        'label': "#000000"
    }
}

def create_color(key: str, theme: dict):
    if not isinstance(theme, dict) or key not in theme:
        return None
    if key == 'name':
        return None
    with Div("flex flex-col gap-2 w-full h-full"):
        lbl = Label(key.title(), "font-medium w-full text-label")
        clr_inp = Input(type='color')
    clr_inp.preview = True    # type: ignore
    try:
        clr_inp.button.classes("border border-black") # type: ignore
    except Exception:
        pass
    clr_inp.set_value(theme.get(key))
    def setValue(e):
        th = getUserStorage().get("theme", {}).copy()
        th[key] = e.value
        if 'name' in getUserStorage().get('theme', {}):
            th.setdefault('name', getUserStorage().get('theme', {}).get('name'))
        updateUserStorage({"theme": th})
        colors(**getUserStorage().get("theme", {}))
    clr_inp.on_value_change(setValue)
    return {key: clr_inp}

def setTheme(value, clr_inps):
    sel = getattr(value, 'value', value)
    preset = PRESETS.get(sel, {})
    base = getUserStorage().get('theme', {}).copy()
    resolved = base.copy()
    for i in clr_inps:
        if not i: continue
        aspect = list(i.keys())[0]
        cinp = list(i.values())[0]
        color_val = preset.get(aspect, base.get(aspect, '#000000'))
        try:
            cinp.set_value(color_val)
        except Exception:
            pass
        resolved[aspect] = color_val
    resolved['name'] = sel
    updateUserStorage({"theme": resolved})
    try:
        colors(**resolved)
    except Exception:
        pass

async def CompTheme(header, footer, drawer):
    header.clear()
    footer.clear()
    footer.set_visibility(False)
    theme_dict = await INIT_THEME()
    theme_dict = theme_dict or {}
    clr_inps = []
    with header: 
        SoftBtn(
            on_click=drawer.toggle,
            icon='menu',
            py=1, px=1
        )
        Label(
            "Configure Theme",
            "text-text-primary text-xl font-bold truncate capitalize"
        )
    with Div("w-full h-full grid grid-cols-1 sm:grid-cols-3 gap-2 sm:gap-4"):
        with Div("flex flex-col gap-2 w-full h-full"):
            Label("Preset", "font-medium w-full text-text-primary")
            Select(
                'w-full text-text-secondary', 
                options=list(PRESETS.keys()), 
                on_change = lambda x, c=clr_inps: setTheme(x, c),
                value=app.storage.user.get("theme", {}).get("name", "Default"),
            )
        for k in list(BASIC.keys()):
            created = create_color(k, theme_dict)
            if created is not None:
                clr_inps.append(created)
