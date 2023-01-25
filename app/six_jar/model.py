
from .. import db, FlaskApp


class Jar(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(10), nullable=False)
    distribution_ratio = db.Column(db.Integer, nullable=False)
    savings = db.relationship('Savings', backref='jar')#1對多 要被參考的表 過去的名稱
    income_and_expense = db.relationship('IncomeAndExpense', backref='jar')  # 1對多 要被參考的表 過去的名稱


class Savings(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    savings = db.Column(db.Integer, nullable=False, default="")#非必填 預設是null, default可改
    jar_id = db.Column(db.Integer, db.ForeignKey('jar.id'))#外來鍵
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))#外來鍵


class IncomeAndExpense(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    income_and_expense = db.Column(db.String(10), nullable=False)
    money = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    remark = db.Column(db.String(100), default="")
    jar_id = db.Column(db.Integer, db.ForeignKey('jar.id'))#外來鍵
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))#外來鍵


class Jars:
    @staticmethod
    def names():
        app = FlaskApp().app
        with app.app_context():
            return [jar.name for jar in Jar.query.order_by(Jar.id).all()]

    @staticmethod
    def length():
        return len(Jar.query.all())

    @staticmethod
    def ratio():
        return [jar.distribution_ratio/100 for jar in Jar.query.order_by(Jar.id).all()]