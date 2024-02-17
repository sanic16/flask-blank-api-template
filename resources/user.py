from flask import request, url_for, redirect
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError

from models.user import User

from schemas.user import UserSchema

from emails import send_email
from utils import generate_confirmation_token, verify_token

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

        token = generate_confirmation_token(email=user.email, salt='activate')
        subject = 'Por favor confirma tu registro'
        link = url_for('useractivateresource', token=token, _external=True)
        body = 'Bienvenido, gracias por registrarte. Por favor confirma tu registro en la siguiente dirección:\n{}'.format(link)
        recipient = user.email 

        send_email(subjet=subject, body=body, recipient=recipient)

        return user_schema.dump(user), HTTPStatus.CREATED
    
class UserActivateResource(Resource):
    def get(self, token):
        email = verify_token(token=token, salt='activate')

        if email is False:
            return {'message': 'El enlace de activación es inválido o ha expirado'}, HTTPStatus.BAD_REQUEST
        
        user = User.get_by_email(email=email)

        if not user:
            return {
                'message': 'El usuario no existe'
            }, HTTPStatus.NOT_FOUND
        
        if user.is_active is True:
            return {
                'message': 'El usuario ya ha sido activado'
            }, HTTPStatus.BAD_REQUEST
        
        user.is_active = True

        user.save()

        return {}, HTTPStatus.NO_CONTENT
        