from flask import Flask

from app.config import get_config
from app.routes.health import health_bp
from app.database import init_db

REQUIRED_SETTINGS = ("SECRET_KEY", "DATABASE_URL")

# Implementing the "Application factory" pattern, it is useful for:
# 1.Tests: every test can create their own clean app with create_app("testing")
# 2. Without circular imports: no module needs to import the "global app"
# 3. Several configurations: dev, test and prod comes from the same function
def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__, static_folder=None) # Pure API, no static files route
    app.config.from_object(get_config(config_name))
    _validate_config(app)

    app.json.sort_keys = False # It keeps our key order in JSON response

    init_db(app) # After validate the config, the engine is created and the session factory and registers the session close at the end of every request.

    # Declaring the API routes
    app.register_blueprint(health_bp)
    return app

def _validate_config(app: Flask) -> None:
    missing = [key for key in REQUIRED_SETTINGS if not app.config.get(key)]
    if missing:
        raise RuntimeError(f"Missing required settings: {', '.join(missing)}. Check your .env file.")