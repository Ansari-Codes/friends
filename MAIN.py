from ENV import FAVICON, APP_NAME, SECRET
import routes, ENV
from nicegui import ui

ui.run(
    favicon=FAVICON, 
    title=APP_NAME,
    storage_secret = SECRET, 
    host=ENV.HOST,
    port=ENV.PORT
    )
