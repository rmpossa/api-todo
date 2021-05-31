from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from app.config import config
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config.from_object(get_config())

    db.init_app(app)

    from app.task_api.api import tasks_bp
    app.register_blueprint(tasks_bp, url_prefix='/tasks')

    db.create_all(app=app)

    CORS(app)

    return app

def get_config():
    return config[os.getenv('FLASK_ENV')]    


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
