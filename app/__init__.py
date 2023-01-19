from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_apispec.extension import FlaskApiSpec
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import MetaData
from flask_migrate import Migrate

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
migrate = Migrate()
bootstrap = Bootstrap()
login_manager = LoginManager()
docs = FlaskApiSpec()