from nicegui import ui, app

def navigate(link: str = '/', new_tab: bool = False):
    ui.navigate.to(link, new_tab=new_tab)
