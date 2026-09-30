import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent # app/config.py
load_dotenv(PROJECT_ROOT / ".env")

def _required(name):
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}, check your .env file.")
    return value

class Config:
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = os.environ.get("DB_PORT", "5432")
    DB_NAME = _required("DB_NAME")
    DB_SCHEMA = _required("DB_SCHEMA")
    DB_USER = _required("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")

    MAX_CONTENT_LENGHT = 1 * 1024 * 1024 # 1M 

class DevelopmentConfig(Config):
    DEBUG = True


# config.py reads the data from .env to use