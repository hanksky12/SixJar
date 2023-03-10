import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_apispec.extension import FlaskApiSpec
from flask_sqlalchemy import SQLAlchemy as BaseSQLAlchemy
from flask_jwt_extended import JWTManager
from sqlalchemy import MetaData
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_login import LoginManager
from contextlib import contextmanager
from celery import Celery
from concurrent.futures import ThreadPoolExecutor
from flask_socketio import SocketIO
from kombu.serialization import register
from celery import Task as TaskBase
from .config import config


class FlaskApp:
    @classmethod
    def create(cls):
        cls.app = Flask(__name__,
                        static_url_path='/static',  # 虛擬靜態路徑
                        static_folder='static/')  # 指定靜態上層根目錄

metadata = MetaData(
    naming_convention={
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
)


class SQLAlchemy(BaseSQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


class Extension:
    def generate_thread_pool(self):
        executor = ThreadPoolExecutor(2)
        return executor

    def generate_sqlalchemy_db(self):
        db = SQLAlchemy(metadata=metadata)
        return db

    def generate_bootstrap(self):
        bootstrap = Bootstrap()
        return bootstrap

    def generate_flaskapispec(self):
        docs = FlaskApiSpec()
        return docs

    def generate_migrate(self):
        migrate = Migrate()
        return migrate

    def generate_jwt(self):
        jwt = JWTManager()
        return jwt

    def generate_login_manager(self):
        login_manager = LoginManager()
        login_manager.login_view = 'user.login3'  # endpoint
        login_manager.login_message = "請先登入"  # 未登入的訊息
        login_manager.login_message_category = "info"  # 未登入的訊息等級
        return login_manager

    def generate_socketio(self):
        socketio = SocketIO()
        return socketio

    def generate_celery(self):
        # 生成worker也是用這一個
        load_dotenv()
        celery = Celery(__name__,
                        broker=config[os.environ["PYTHON_WEB_CONFIG"]].CELERY_BROKER_URL,
                        result_backend=config[os.environ["PYTHON_WEB_CONFIG"]].CELERY_RESULT_BACKEND)

        celery.autodiscover_tasks(['app.celery_task'])  # 註冊任務，去指定有任務的模組（從下命令的視角開始），自動從裡面找tasks.py
        celery.conf.update(vars(config[os.environ["PYTHON_WEB_CONFIG"]]))
        #針對pytohn物件用pickle序列化(not jason)
        register('pickle', lambda buf: buf, lambda buf: buf, content_type='application/x-python-serialize')
        # FlaskApp().create()
        # app = FlaskApp().app
        # class ContextTask(TaskBase):
        #     abstract = True
        #     def __call__(self, *args, **kwargs):
        #         with app.app_context():
        #             return TaskBase.__call__(self, *args, **kwargs)
        #
        # celery.Task = ContextTask
        return celery
