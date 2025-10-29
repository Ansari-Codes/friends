import uuid, os

# RUN OPTIONS
FAVICON = "☕"
APP_NAME = "Friends"
# HOST = '127.0.0.1'
# PORT = int(os.environ.get("PORT", 8080))
SECRET = str(uuid.uuid4().hex)

# THEME
THEME_DEFAULT = dict(
    primary = "#0E6E43",
    secondary = "#75b78c",
    accent = '#9c27b0',
    dark = '#1d1d1d',
    success = '#21ba45',
    error = '#c10015',
    info = '#31ccec',
    warning = '#f2c037',
    btn = "#639761",
    disabled = "#6B6B6B",
    inp = "#B1D2B0",
    # Chat-specific additions
    chat_bubble_sent = '#5898d4',
    chat_bubble_received = '#f0f0f0',
    chat_background = '#ffffff',
    chat_input_bg = '#f8f9fa',
    text_primary = '#1d1d1d',
    text_secondary = '#6c757d',
    online_indicator = '#21ba45',
    typing_indicator = '#f2c037',
    unread_badge = '#c10015',
)
DB_CREDS = dict(
    ENGINE = 'sqlite',
    NAME = "database.sqlite",
)

MIGRATIONS_FOLDER = "db.Migrations"
