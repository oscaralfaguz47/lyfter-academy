import logging

from flask import Flask

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

    @app.route("/health")
    def health():
        with db.get_connection().cursor() as cursor:
            cursor.execute("SELECT 1") # Just proves the DB answers
        return {"status": "ok"}

    return app