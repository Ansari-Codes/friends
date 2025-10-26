from nicegui import ui

def message(**kwargs):
    return ui.chat_message(text_html=True, sanitize=lambda x: x, **kwargs)

