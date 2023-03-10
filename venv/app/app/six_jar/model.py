from sqlalchemy.exc import OperationalError
from sqlalchemy import event
import os

from .. import db
from ..extension import FlaskApp
from ..config import config
from ..db_init_data import jar_dict


class Jar(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(10), nullable=False)
    distribution_ratio = db.Column(db.Integer, nullable=False)
    savings = db.relationship('Savings', backref='jar')  # 1對多 要被參考的表 過去的名稱
    income_and_expense = db.relationship('IncomeAndExpense', backref='jar')  # 1對多 要被參考的表 過去的名稱


class Savings(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    savings = db.Column(db.Integer, nullable=False, default="")  # 非必填 預設是null, default可改
    jar_id = db.Column(db.Integer, db.ForeignKey('jar.id'))  # 外來鍵
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 外來鍵


class IncomeAndExpense(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    income_and_expense = db.Column(db.String(10), nullable=False)
    money = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    remark = db.Column(db.String(100), default="")
    jar_id = db.Column(db.Integer, db.ForeignKey('jar.id'))  # 外來鍵
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 外來鍵


@event.listens_for(Jar.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    if len(Jar.query.all()) == 0:
        jar_list = [Jar(name=key, distribution_ratio=value) for key, value in jar_dict.items()]
        db.session.add_all(jar_list)
        db.session.commit()

FlaskApp().create()
with FlaskApp().app.app_context():
    FlaskApp().app.config.from_object(config[os.environ["PYTHON_WEB_CONFIG"]])
    db.init_app(FlaskApp().app)
    db.create_all()


class Jars:
    @staticmethod
    def names():
        with FlaskApp().app.app_context():
            return [jar.name for jar in Jar.query.order_by(Jar.id).all()]

    @staticmethod
    def length():
        return len(Jar.query.all())

    @staticmethod
    def ratio():
        return [jar.distribution_ratio / 100 for jar in Jar.query.order_by(Jar.id).all()]
