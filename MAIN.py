import asyncio

# MIGRATIONS
from db.db import RUN_SQL
from db.Migrations.CreateTableChat import up as ccup
from db.Migrations.CreateTableUsers import up as ctup

sql = ccup() + '\n' + ctup()
asyncio.run(RUN_SQL(sql))

# MAIN APP
from ENV import FAVICON, APP_NAME, SECRET
import routes, ENV
from nicegui import ui

ui.run(
    favicon=FAVICON, 
    title=APP_NAME,
    storage_secret = SECRET, 
    host=ENV.HOST,
    port=ENV.PORT,
    reload=False,
    )
