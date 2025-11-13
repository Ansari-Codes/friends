import logging

logging.basicConfig(
    level=logging.DEBUG,  # or DEBUG for more verbose
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# MIGRATIONS
from db.Migrations.CreateTableChat import up as ccup
from db.Migrations.CreateTableUsers import up as ctup

sql = ccup() + '\n' + ctup()
API_URL = "http://worldofansari.com/dbapi"
payload = {"query": sql, "to_fetch": False, "name": "friends"}
try:
    logger.info("Applying migrations...")
    with httpx.Client(timeout=20) as client:
        response = client.post(API_URL, json=payload)
        response.raise_for_status()
    logger.info("Applied migrations successfully")
except httpx.HTTPStatusError as e:
    logger.error(f"HTTP error while calling API: {e.response.status_code} - {e.response.text}")
    raise
except httpx.RequestError as e:
    logger.error(f"Request failed: {e}")
    raise
except Exception as e:
    logger.exception("Unexpected error in RUN_SQL")
    raise

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
