from ENV import FAVICON, APP_NAME, SECRET
import routes
from nicegui import ui

ui.run(
    favicon=FAVICON, title=APP_NAME,
    storage_secret = SECRET,
    on_air=True,
    )
