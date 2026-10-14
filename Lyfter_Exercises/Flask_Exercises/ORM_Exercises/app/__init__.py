from flask import Flask

from app.config import get_config
from app.routes.health import health_bp
from app.routes.users import users_bp
from app.database import init_db
from app.errors.handlers import register_error_handlers
from app.hooks import register_hooks
from app.logging_config import configure_logging

REQUIRED_SETTINGS = ("SECRET_KEY", "DATABASE_URL")

# Implementing the "Application factory" pattern, it is useful for:
# 1.Tests: every test can create their own clean app with create_app("testing")
# 2. Without circular imports: no module needs to import the "global app"
# 3. Several configurations: dev, test and prod comes from the same function
def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__, static_folder=None) # Pure API, no static files route
    app.config.from_object(get_config(config_name))
    _validate_config(app)

    # Setup logging before anything logs
    configure_logging(app.config["LOG_LEVEL"]) 

    app.json.sort_keys = False # It keeps our key order in JSON response

    # After validate the config, the engine is created and the session factory and registers the session close at the end of every request.
    init_db(app) 
    # request ID, timing and headers on every request
    register_hooks(app)
    # Here we register the handlers that turn every error raised in the API into a "JSON response"
    register_error_handlers(app)

    # Declaring the API routes
    app.register_blueprint(health_bp)
    app.register_blueprint(users_bp)
    return app

def _validate_config(app: Flask) -> None:
    missing = [key for key in REQUIRED_SETTINGS if not app.config.get(key)]
    if missing:
        raise RuntimeError(f"Missing required settings: {', '.join(missing)}. Check your .env file.")