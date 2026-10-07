import logging
from flask import Flask

from app.http.errors import register_error_handlers
from app import db
from app.config import DevelopmentConfig


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.json.sort_keys = False

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s"
    )

    db.init_app(app)
    register_error_handlers(app)

    # Import all handlers, after db.init_app to avoid circular imports
    from app.routes.users import users_bp
    from app.routes.vehicles import vehicles_bp
    from app.routes.rentals import rentals_bp
    from app.routes.backup import backup_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(vehicles_bp)
    app.register_blueprint(rentals_bp)
    app.register_blueprint(backup_bp)

    return app