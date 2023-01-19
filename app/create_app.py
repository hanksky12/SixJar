from flask import Flask
from dotenv import load_dotenv
import os


from . import db, login_manager, bootstrap, migrate
from .config import config

def create_app():
    load_dotenv()
    app = Flask(__name__,
                static_url_path='/static',#虛擬靜態路徑
                static_folder='static/')#指定靜態上層根目錄
    app.config.from_object(config[os.getenv("PYTHON_WEB_CONFIG")])

    db.init_app(app)
    migrate.init_app(app, db)
    # login_manager.init_app(app)
    bootstrap.init_app(app)


    #避免循環import
    from .main import main_bp
    app.register_blueprint(main_bp)

    from .user import user_bp
    app.register_blueprint(user_bp, url_prefix='/user')

    from .six_jar import six_jar_bp
    app.register_blueprint(six_jar_bp, url_prefix='/six_jar')

    from .api.v1 import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    # 分之路由要先註冊，文件初始化才抓得到
    # docs.init_app(app)

    return app