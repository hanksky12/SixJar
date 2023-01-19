import os
import datetime


from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    RESTFUL_JSON = {'default': str}
    APISPEC_SPEC=APISpec(
        title='六個罐子api官方文件',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    )
    APISPEC_SWAGGER_URL= '/apispec_json/'  # URI to access API Doc JSON
    APISPEC_SWAGGER_UI_URL= '/apispec/'  # URI to access UI of API Doc


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SECRET_KEY = 'THIS IS Fix'



class ProductionConfig(BaseConfig):
    DEBUG = False
    SECRET_KEY = 'THIS IS Fix'



config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
