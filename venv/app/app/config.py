import os
import datetime
import sqlalchemy
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

basedir = os.path.abspath(os.path.dirname(__file__))
db_user = os.getenv("DB_USER", "")
db_pass = os.getenv("DB_PASS", "")
db_name = os.getenv("DB_NAME", "")
db_host = os.getenv("DB_HOST", "")
unix_socket_path = os.getenv("INSTANCE_UNIX_SOCKET", "")


# print(f'mysql+pymysql://{db_user}:{db_pass}@{db_host}:3306/{db_name}')


class BaseConfig:
    HOST = 'localhost'
    PORT = '8080'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 減少SQLALCHEMY記憶體消耗
    SESSION_PROTECTION = 'strong'  # 設置flask-login中對session的安全等級設置
    RESTFUL_JSON = {'default': str}
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_ACCESS_COOKIE_PATH = '/'  # 只有在這個網址下 才送出jwt cookie  後面加什麼不重要/api/dsfdsdffd
    JWT_REFRESH_COOKIE_PATH = '/api/v1/token/refresh'  # 只有在這個網址下 才送出jwt refresh cookie
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=20)  # 過期時間
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=30)  # 過期時間
    CELERY_BROKER_URL = 'redis://localhost:6379/0'  # 往哪邊發送
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'  # 到哪邊拿
    CELERY_TIMEZONE = 'Asia / Taipei'

    APISPEC_SPEC = APISpec(
        title='🐾六個罐子🐾Api文件',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    )
    APISPEC_SWAGGER_URL = '/apispec_json/'  # URI to access API Doc JSON
    APISPEC_SWAGGER_UI_URL = '/apispec/'  # URI to access UI of API Doc


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(basedir, '../project.db')
    DEBUG = True
    SECRET_KEY = 'THIS IS Fix'
    JWT_SECRET_KEY = 'THIS IS Fix'
    # JWT_COOKIE_SECURE = True


class LocalTestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(basedir, '../test.db')
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=60)  # 過期時間
    DEBUG = True
    SECRET_KEY = 'THIS IS Fix'
    JWT_SECRET_KEY = 'THIS IS Fix'
    JWT_COOKIE_SECURE = False


class CloudTestConfig(BaseConfig):
    SERVER_NAME = 'localhost:8080'
    SQLALCHEMY_DATABASE_URI = sqlalchemy.engine.url.URL.create(
        drivername="mysql+pymysql",
        username=db_user,
        password=db_pass,
        database=db_name,
        query={"unix_socket": unix_socket_path},
    )

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 5,
        "max_overflow": 2,
        "pool_timeout": 30,
        "pool_recycle": 1800
    }  # create_engine 的參數
    DEBUG = False
    SECRET_KEY = os.urandom(10)
    JWT_SECRET_KEY = os.urandom(10)
    JWT_COOKIE_SECURE = True


class DockerTestConfig(BaseConfig):
    HOST = '0.0.0.0'
    PORT = '8080'
    # db_host 用docker 裡面db的名城
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{db_user}:{db_pass}@{db_host}:3306/{db_name}'
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 5,
        "max_overflow": 2,
        "pool_timeout": 30,
        "pool_recycle": 1800
    }  # create_engine 的參數
    DEBUG = False
    SECRET_KEY = os.urandom(10)
    JWT_SECRET_KEY = os.urandom(10)
    # JWT_COOKIE_SECURE = True
    CELERY_BROKER_URL = 'redis://redis:6379/0'  # 往哪邊發送  'redis://docker_redis_name:6379/0'
    CELERY_RESULT_BACKEND = 'redis://redis:6379/0'  # 到哪邊拿
    REDIS_URL = 'redis://redis:6379/0'


class ProductionConfig(BaseConfig):
    DEBUG = False
    SECRET_KEY = os.urandom(10)
    JWT_SECRET_KEY = os.urandom(10)
    JWT_COOKIE_SECURE = True  # 打開cookie的httpOnly 1.不讓ＪＳ使用cookie 2.只有在https下 才送出jwt cookie


config = {
    'development': DevelopmentConfig,
    "local_test": LocalTestConfig,
    "test": CloudTestConfig,
    "docker_test": DockerTestConfig,
    'production': ProductionConfig,
}
