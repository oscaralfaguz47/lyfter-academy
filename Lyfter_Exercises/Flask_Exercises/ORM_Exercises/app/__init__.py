from flask import Flask

from app.config import get_config
from app.routes.health import health_bp

REQUIRED_SETTINGS = ("DATABASE_URL")

def create_app(config_name:str | None = None) -> Flask:
    app = Flask(__name__, static_folder=None) # Pure API, no static files route
    app.config.from_object(get_config(config_name))
    _validate_config(app)