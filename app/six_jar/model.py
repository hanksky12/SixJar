from .. import db


class Jar(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(10), nullable=False)
    savings = db.relationship('Savings', backref='jar')#1對多 要被參考的表 過去的名稱


class Savings(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    savings = db.Column(db.Integer, nullable=False, default="")#非必填 預設是null, default可改
    distribution_ratio = db.Column(db.Integer, nullable=False)
    jar_id = db.Column(db.Integer, db.ForeignKey('jar.id'))#外來鍵
