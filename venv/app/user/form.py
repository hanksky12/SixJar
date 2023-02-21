from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError, IntegerField, BooleanField
from wtforms.validators import DataRequired
from wtforms import validators
from wtforms.fields import EmailField
import email_validator

from .model import User


class EmailForm(FlaskForm):
    email = EmailField('Email', validators=[
        DataRequired(),
        validators.Length(1, 50),
        validators.Email(message="無效信箱")
    ])


class NameForm(FlaskForm):
    name = StringField('姓名', validators=[DataRequired()])


class PasswordForm(FlaskForm):
    password = PasswordField('密碼', validators=[
        DataRequired(),
        validators.Length(2, 10)
    ])


class UserInfoForm(NameForm, PasswordForm):
    password2 = PasswordField('重複密碼', validators=[
        DataRequired(),
        validators.EqualTo('password', '輸入的兩次密碼不相等')])
    submit = SubmitField('修改')


class LoginForm(EmailForm, PasswordForm):
    remember_me = BooleanField("記住我")
    submit = SubmitField('登入')


class RegisterForm(EmailForm, UserInfoForm):
    submit = SubmitField('註冊為會員')

    def validate_email(self, mail):  # 自定義驗證的項目 開頭validate 結尾要欄位名稱
        if User.query.filter_by(email=mail.data).first():
            raise ValidationError('Mail已被註冊')
