from flask import request, url_for, redirect
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError

from models.user import User

from schemas.user import UserSchema, UpdatePasswordSchema

import secrets

from emails import send_email
from utils import generate_confirmation_token, verify_token, hash_password, check_password

user_schema = UserSchema()
user_public_schema = UserSchema(exclude=('email', 'is_admin', 'updated_at'))

update_password_schema = UpdatePasswordSchema()

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

        token = generate_confirmation_token(user.email, salt='activate')
        subject = 'Por favor confirma tu registro'
        link = url_for('useractivateresource', token=token, _external=True)
        body = 'Bienvenido, gracias por registrarte. Por favor confirma tu registro en la siguiente dirección:\n{}'.format(link)
        recipient = user.email 

        send_email(subjet=subject, body=body, recipient=recipient)

        return user_schema.dump(user), HTTPStatus.CREATED

class UserRecoverResource(Resource):
    def post(self):
        json_data = request.get_json()

        try:
            data = user_schema.load(data=json_data, partial=('username', 'password'))
        except ValidationError as error:
            return {
                'message': 'Error al validar los datos',
                'errors': error.messages
            }
        
        user = User.get_by_email(data.get('email'))

        if user is None:
            return {'message': 'El usuario no existe'}, HTTPStatus.NOT_FOUND
        
        email = user.email
        new_password = secrets.token_urlsafe(8) 
        token = generate_confirmation_token(email, new_password, salt='recover')
        subject = 'Recuperación de contraseña'
        link = url_for('userpasswordresource', token=token, _external=True)
        body = 'Hola, si solicitaste recuperar tu contraseña, tu nueva contraseña es: {}. Si no solicitaste recuperar tu contraseña, por favor ignora este mensaje. El enlace para cambiar tu contraseña es: {}'.format(new_password, link)
        recipient = email

        send_email(
            subjet=subject,
            body=body,
            recipient=recipient
        )

        return {}, HTTPStatus.NO_CONTENT




    
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
        
class UserPasswordResource(Resource):
    def get(self, token):
        
        keys = verify_token(token=token, salt='recover')

        if keys is False:
            return {
                'message': 'El enlace de recuperación de contraseña es inválido o ha expirado'
            }, HTTPStatus.BAD_REQUEST
        
        email, new_password = keys

        user = User.get_by_email(email)

        if user is None:
            return {
                'message': 'El usuario no existe'
            }, HTTPStatus.NOT_FOUND
        

        user.password = hash_password(new_password)  
        user.save()

        return {}, HTTPStatus.NO_CONTENT
    
class UserChangePasswordResource(Resource):
    @jwt_required(fresh=True)
    def put(self):
        json_data = request.get_json()
        
        current_user = get_jwt_identity()

        try:
            data = update_password_schema.load(data=json_data)
        except ValidationError as error:
            return {
                'message': 'Error al validar credenciales',
                'errors': error.messages
            }
        
        
        
        user = User.get_by_id(user_id=current_user)

        if user is None:
            return {
                'message': 'El usuario no existe',
            }, HTTPStatus.NOT_FOUND
        
        if not check_password(data.get('password'), user.password):
            return {
                'message': 'Credenciales incorrectas',
            }, HTTPStatus.UNAUTHORIZED
        
        if data.get('newPassword') != data.get('confirmPassword'):
            return {
                'message': 'Las contraseñas no coinciden'
            }, HTTPStatus.BAD_REQUEST

        user.password = hash_password(data.get('newPassword'))
        user.save()

        return {}, HTTPStatus.NO_CONTENT
    
class UserResource(Resource):
    @jwt_required(optional=True)
    def get(self, username):
        user = User.get_by_username(username=username)

        if user is None:
            return {'message': 'usuario no encontrado'}, HTTPStatus.NOT_FOUND
        
        current_user = get_jwt_identity()

        if current_user == user.id:
            data = user_schema.dump(user)
        else:
            data = user_public_schema.dump(user)
        
        return data, HTTPStatus.OK

class MeResource(Resource):
    @jwt_required()
    def get(self):
        user = User.get_by_id(user_id=get_jwt_identity())

        return user_schema.dump(user), HTTPStatus.OK
    


        
    
