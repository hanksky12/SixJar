import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_apispec.extension import FlaskApiSpec
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from sqlalchemy import MetaData
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_login import LoginManager

from .config import config

metadata = MetaData(
    naming_convention={
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
    }
)
db = SQLAlchemy(metadata=metadata)
bootstrap = Bootstrap()
docs = FlaskApiSpec()
migrate = Migrate()
jwt = JWTManager()
login_manager = LoginManager()
login_manager.login_view = 'user.login3' #endpoint



class FlaskApp:
    @classmethod
    def create(cls):
        cls.app = Flask(__name__,
                    static_url_path='/static',  # 虛擬靜態路徑
                    static_folder='static/')  # 指定靜態上層根目錄



def create_app():
    load_dotenv()
    FlaskApp().create()
    app = FlaskApp().app
    jwt.init_app(app)
    app.config.from_object(config[os.getenv("PYTHON_WEB_CONFIG")])
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    #避免循環import
    from .main import main_bp
    app.register_blueprint(main_bp)

    from .user import user_bp
    app.register_blueprint(user_bp, url_prefix='/user')

    from .six_jar import six_jar_bp
    app.register_blueprint(six_jar_bp, url_prefix='/six_jar')

    from .api.v1 import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')


    # 分之路由要先註冊，資料庫model 才抓得到有被 import，文件初始化才抓得到
    # with app.app_context():
    #     db.create_all()

    # docs.init_app(app)


    return app