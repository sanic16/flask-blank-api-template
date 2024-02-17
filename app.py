from flask import Flask
from flask_migrate import Migrate

from extensions import db, jwt

from flask_restful import Api

from config import Config

from models.user import User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_extensions(app=app)
    register_resources(app=app)
    return app


def register_extensions(app):
    db.init_app(app=app)
    jwt.init_app(app=app)
    migrate = Migrate(app=app, db=db)

def register_resources(app):
    api = Api(app=app)    

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)