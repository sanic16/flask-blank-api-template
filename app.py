from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from config import Config

from extensions import db, jwt, mail

from resources.user import (UserListResource, UserActivateResource, UserRecoverResource, UserPasswordResource, 
                            UserChangePasswordResource)
from resources.token import (TokenResource)

from models.token import TokenBlocklist


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_extensions(app=app)
    register_resources(app=app)
    return app


def register_extensions(app):
    db.init_app(app=app)
    jwt.init_app(app=app)
    mail.init_app(app=app)
    migrate = Migrate(app=app, db=db)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload: dict) -> bool:
        jti = jwt_payload['jti']
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
        return token is not None

def register_resources(app):
    api = Api(app=app)

    api.add_resource(UserListResource, '/api/users')   
    api.add_resource(UserChangePasswordResource, '/api/users/change-password')

    api.add_resource(UserActivateResource, '/api/users/activate/<string:token>')
    api.add_resource(UserRecoverResource, '/api/users/recover')
    api.add_resource(UserPasswordResource, '/api/users/password/<string:token>')

    api.add_resource(TokenResource, '/api/token') 

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)