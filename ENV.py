import uuid, os

# RUN OPTIONS
FAVICON = "☕"
APP_NAME = "Friends"
QUOTE = "Connections that last a lifetime!"
HOST = '0.0.0.0'
PORT = int(os.environ.get("PORT", 8080))
SECRET = str(uuid.uuid4().hex)

# THEME
BASIC = dict(
    name = 'Default',
    primary = "#0E6E43",
    secondary = "#75b78c",
    accent = "#9ac6bb",
    btn = "#639761",
    inp = "#B1D2B0",
    success = '#21ba45',
    error = '#c10015',
    info = '#31ccec',
    warning = '#f2c037',
    card = "#b1d2ac",
    label = "#000000",
)
BASIC.update({
            "text-primary": "#ffffff", 
            "text-secondary": "#000000"
        })

THEME_DEFAULT = dict()
THEME_DEFAULT.update(BASIC)

DB_CREDS = dict(
    ENGINE = 'sqlite',
    NAME = "database.sqlite",
)

MIGRATIONS_FOLDER = "db.Migrations"
