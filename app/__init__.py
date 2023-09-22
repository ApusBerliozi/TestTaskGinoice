from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from swagger_ui import api_doc

from app.api_spec import CreateUserRequest, CreateTokenRequest, GetUserResponse

db = SQLAlchemy()
host = "localhost"
port = 9000


def init_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_pyfile('config/config.py')
    db.init_app(app)
    api_doc(app, config_url=f'http://{host}:{port}/api/spec', url_prefix='/api/doc', title='API doc')
    with app.app_context():
        from . import endpoints
        db.create_all()
        return app
