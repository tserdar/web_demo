"""Script to create the webapp."""

from pathlib import Path

from flask import Flask

from app.routes import main


def my_web_app() -> Flask:
    """Create the webapp."""
    app = Flask(__name__)

    upload_path = Path("app") / "static" / "uploads"
    upload_path.mkdir(exist_ok=True, parents=True)

    results_path = Path("app") / "static" / "results"
    results_path.mkdir(exist_ok=True, parents=True)

    app.config["UPLOAD_FOLDER"] = upload_path
    app.config["RESULTS_FOLDER"] = results_path

    app.register_blueprint(main)

    return app
