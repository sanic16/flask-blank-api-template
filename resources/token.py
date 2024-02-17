from http import HTTPStatus
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from models.user import User
from schemas.user import UserSchema

from utils import check_password

user_schema = UserSchema()

class TokenResource(Resource):
    def post(self):
        json_data = request.get_json()
        email = json_data.get('email')
        password = json_data.get('password')
        user = User.get_by_email(email=email)

        if not user or not check_password(password, user.password):
            return {'message': 'Correo o contraseña incorrectos'}, HTTPStatus.UNAUTHORIZED
        
        # if user.is_active is False:
        #     return {'message': 'Usuario inactivo'}, HTTPStatus.FORBIDDEN
        
        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id)

        user = user_schema.dump(user)

        return {
            'user': user,
            'access_token': access_token,
            'refresh_token': refresh_token
        }, HTTPStatus.OK

