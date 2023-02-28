import os

from dotenv import load_dotenv

load_dotenv()

POSTGRES_CONNECTION_SETTINGS = {
    "host": os.environ.get("DB_HOST"),
    "port": os.environ.get("DB_PORT"),
    "dbname": os.environ.get("DB_NAME"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
}

SQLITE_DB_FILE = os.environ.get("SQLITE_DB_FILE")
