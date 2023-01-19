
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,ValidationError
from wtforms.validators import DataRequired
from wtforms.fields import EmailField









class EmailForm(FlaskForm):
    EmailField('Email', validators=WtfFormSetting.validators + [
        validators.Length(1, 50),
        validators.Email(message="無效信箱")
    ])


class LoginForm(FlaskForm):
    name = StringField('姓名', validators=[DataRequired()])
    password = PasswordField('密碼', validators=[DataRequired()])
    submitfield = SubmitField('提交')


class RegisterForm(EmailForm):
    submit = SubmitField('註冊為會員')

    def validate_email(self, mail):# 自定義驗證的項目 開頭validate 結尾要欄位名稱
        if User.query.filter_by(email=mail.data).first():
            raise ValidationError('Mail已被註冊')

