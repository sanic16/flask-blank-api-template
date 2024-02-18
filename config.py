from dotenv import load_dotenv
import os

load_dotenv()

mysql_db = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_DATABASE')
}

class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
        mysql_db['user'],
        mysql_db['password'],
        mysql_db['host'],
        mysql_db['port'],
        mysql_db['database']
    ) 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '5662fcfc2440c9f5ce09ecf4c45e0d31'
    JWT_ERROR_MESSAGE_KEY = 'message'
    JWT_ACCESS_TOKEN_EXPIRES = 60 * 15 # 15 minutos
    JWT_REFRESH_TOKEN_EXPIRES = 60 * 60 * 24 * 7 # 7 días
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    JWT_ACCESS_COOKIE_NAME = 'access_token'
    JWT_REFRESH_COOKIE_NAME = 'refresh_token'
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_SAMESITE = 'None'
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_TOKEN_LOCATION = ['headers', 'cookies'] 

    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'apikey'
    MAIL_PASSWORD = os.getenv('SENDGRID_API_KEY')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
