from werkzeug.security import generate_password_hash,  check_password_hash
from flask_login import UserMixin
from .. import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(400), nullable=False)
    savings = db.relationship('Savings', backref='user')  # 1對多 要被參考的表 過去的名稱
    income_and_expense = db.relationship('IncomeAndExpense', backref='user')  # 1對多 要被參考的表 過去的名稱

    def check_password(self, password):
        return check_password_hash(self.password, password)


