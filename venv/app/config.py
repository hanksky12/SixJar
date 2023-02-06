import os
import datetime


from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False #減少SQLALCHEMY記憶體消耗
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(basedir, 'project.db')
    SESSION_PROTECTION = 'strong' #設置flask-login中對session的安全等級設置
    RESTFUL_JSON = {'default': str}
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_ACCESS_COOKIE_PATH = '/'  # 只有在這個網址下 才送出jwt cookie  後面加什麼不重要/api/dsfdsdffd
    JWT_REFRESH_COOKIE_PATH = '/api/v1/token/refresh'  # 只有在這個網址下 才送出jwt refresh cookie
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=2)  # 過期時間
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=30)  # 過期時間


    APISPEC_SPEC=APISpec(
        title='🐾六個罐子🐾Api文件',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    )
    APISPEC_SWAGGER_URL= '/apispec_json/'  # URI to access API Doc JSON
    APISPEC_SWAGGER_UI_URL= '/apispec/'  # URI to access UI of API Doc


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SECRET_KEY = 'THIS IS Fix'
    JWT_SECRET_KEY = 'super-secret'
    JWT_COOKIE_SECURE = False

class ProductionConfig(BaseConfig):
    DEBUG = False
    SECRET_KEY = os.urandom(10)
    JWT_SECRET_KEY = os.urandom(10)
    JWT_COOKIE_SECURE = True# 打開cookie的httpOnly 1.不讓ＪＳ使用cookie 2.只有在https下 才送出jwt cookie



config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
