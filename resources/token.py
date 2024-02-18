from http import HTTPStatus
from flask import request, current_app, make_response
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from models.user import User
from models.token import TokenBlocklist
from schemas.user import UserSchema
import os

from utils import check_password
from marshmallow import ValidationError
from dotenv import load_dotenv
from extensions import db

from datetime import datetime, timezone

load_dotenv()

user_schema = UserSchema()

class TokenResource(Resource):
    def post(self):
        json_data = request.get_json()
        
        try:
            data = user_schema.load(data=json_data, partial=('username',))
        except ValidationError as error:
            return {
                'message': 'Credenciales imcompletas',
                'errors': error.messages
            }, HTTPStatus.BAD_REQUEST
        
        email = data.get('email')
        password = json_data.get('password')

        user = User.get_by_email(email=email)

        if user is None or not check_password(password, user.password):
            return {'message': 'Credenciales incorrectas'}, HTTPStatus.UNAUTHORIZED
        
        if user.is_active is False:
            return {'message': 'Usuario inactivo'}, HTTPStatus.FORBIDDEN
        
        
        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id)

        user = user_schema.dump(user)


        access_token_expire = current_app.config.get('JWT_ACCESS_TOKEN_EXPIRES')
        refresh_token_expire = current_app.config.get('JWT_REFRESH_TOKEN_EXPIRES')

        secure = os.getenv('ENVIRONMENT') == 'production'

        response = make_response(user, HTTPStatus.OK)
        response.set_cookie('access_token', access_token, httponly=True, samesite='None', secure=secure, expires=access_token_expire)
        response.set_cookie('refresh_token', refresh_token, httponly=True, samesite='None', secure=secure, expires=refresh_token_expire) 
        return response

class RefreshResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user, fresh=False)

        user = User.get_by_id(user_id=current_user)

        user = user_schema.dump(user)

        access_token_expire = current_app.config.get('JWT_ACCESS_TOKEN_EXPIRES')
        
        secure = os.getenv('ENVIRONMENT') == 'production'

        response = make_response(user, HTTPStatus.OK)
        response.set_cookie('access_token', access_token, httponly=True, samesite='None', secure=secure, expires=access_token_expire)
        return response
    
class RevokeResource(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        now = datetime.now(timezone.utc)
        db.session.add(TokenBlocklist(jti=jti, created_at=now))
        db.session.commit()

        return {'message': 'Se ha revocado el token'}, HTTPStatus.OK

