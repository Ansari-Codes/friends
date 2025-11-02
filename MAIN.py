from ENV import FAVICON, APP_NAME, SECRET
import routes, ENV
from nicegui import ui
from db.migrate import apply_migrations
import asyncio

asyncio.run(apply_migrations())
ui.run(
    favicon=FAVICON, 
    title=APP_NAME,
    storage_secret = SECRET, 
    host=ENV.HOST,
    port=ENV.PORT
    )
