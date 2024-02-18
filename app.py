from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from config import Config

from extensions import db, jwt, mail

from resources.user import (UserListResource, UserActivateResource, UserRecoverResource, UserPasswordResource, 
                            UserChangePasswordResource, UserResource, MeResource)
from resources.token import (TokenResource, RefreshResource, RevokeResource, RevokeRefreshResource,
                            TokenMobileResource, RefreshMobileResource)

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

    api.add_resource(UserListResource, '/api/v1/users')   
    api.add_resource(UserChangePasswordResource, '/api/v1/users/change-password')
    api.add_resource(UserResource, '/api/v1/users/<string:username>')
    api.add_resource(MeResource, '/api/v1/users/me')

    api.add_resource(UserActivateResource, '/api/v1/users/activate/<string:token>')
    api.add_resource(UserRecoverResource, '/api/v1/users/recover')
    api.add_resource(UserPasswordResource, '/api/v1/users/password/<string:token>')

    api.add_resource(TokenResource, '/api/v1/token') 
    api.add_resource(RefreshResource, '/api/v1/refresh')
    api.add_resource(RevokeResource, '/api/v1/revoke')
    api.add_resource(RevokeRefreshResource, '/api/v1/revoke-refresh')
    
    # Mobile
    api.add_resource(TokenMobileResource, '/api/v1/mobile/token')
    api.add_resource(RefreshMobileResource, '/api/v1/mobile/refresh')

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)