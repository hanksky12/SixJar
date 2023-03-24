import os
from dotenv import load_dotenv
from .config import config
from .extension import Extension, FlaskApp

extension = Extension()
executor = extension.generate_thread_pool()
db = extension.generate_sqlalchemy_db()
bootstrap = extension.generate_bootstrap()
docs = extension.generate_flaskapispec()
migrate = extension.generate_migrate()
jwt = extension.generate_jwt()
login_manager = extension.generate_login_manager()
socketio = extension.generate_socketio()
celery = extension.generate_celery()
redis = extension.generate_redis()
cache = extension.generate_cache()
debug_toolbar = extension.generate_debug_toolbar()


def create_app():
    load_dotenv()
    FlaskApp().create()
    app = FlaskApp().app
    app.config.from_object(config[os.environ["PYTHON_WEB_CONFIG"]])
    for __object in [jwt, bootstrap, db, login_manager, socketio, cache, debug_toolbar]:
        __object.init_app(app)
    migrate.init_app(app, db)

    # 避免循環import
    from .main import main_bp
    app.register_blueprint(main_bp)

    from .user import user_bp
    app.register_blueprint(user_bp, url_prefix='/user')

    from .six_jar import six_jar_bp
    app.register_blueprint(six_jar_bp, url_prefix='/six-jar')

    from .api.v1 import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    from .commands import commands_bp
    app.register_blueprint(commands_bp)

    # 分之路由要先註冊，資料庫model 才抓得到有被 import，文件初始化才抓得到
    with app.app_context():
        db.create_all()

    docs.init_app(app)
    app.run(host=config[os.environ["PYTHON_WEB_CONFIG"]].HOST, port=config[os.environ["PYTHON_WEB_CONFIG"]].PORT)
    return app
