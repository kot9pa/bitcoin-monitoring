import os
from dotenv import load_dotenv

if load_dotenv():
    WEB_PORT = os.environ.get("WEB_PORT")
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT")
    DB_NAME = os.environ.get("DB_NAME")
    DB_USER = os.environ.get("DB_USER")
    DB_PASS = os.environ.get("DB_PASS")
    DB_PATH = f"{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

db_url = f"postgres://{DB_PATH}"
config = {
    "connections": {"master": db_url},
    "apps": {
        "models": {
            "models": ["models"],
            "default_connection": "master",
        }
    },
    "use_tz": False,
    "timezone": "UTC",
}