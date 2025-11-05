from ENV import FAVICON, APP_NAME, SECRET
import routes, ENV
from nicegui import ui
import asyncio

ui.run(
    favicon=FAVICON, 
    title=APP_NAME,
    storage_secret = SECRET, 
    host=ENV.HOST,
    port=ENV.PORT,
    reload=True,
    )
