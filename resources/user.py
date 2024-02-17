from flask import request
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError

from models.user import User

from schemas.user import UserSchema

user_schema = UserSchema()

class UserListResource(Resource):
    def post(self):
        json_data = request.get_json()

        try:
            data = user_schema.load(data=json_data)
        except ValidationError as error:
            return {
                'message': 'Error al validar los datos',
                'errors': error.messages
            }, HTTPStatus.BAD_REQUEST
        
        if User.get_by_username(data.get('username')):
            return {'message': 'El usuario ya existe'}, HTTPStatus.BAD_REQUEST
        
        if User.get_by_email(data.get('email')):
            return {'message': 'El correo ya se encuentra registrado'}, HTTPStatus.BAD_REQUEST
        
        user = User(**data)
        user.save()

        return user_schema.dump(user), HTTPStatus.CREATED