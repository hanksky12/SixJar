from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, \
    ValidationError, IntegerField, DateField, SelectField, TextAreaField
from wtforms.validators import DataRequired
from wtforms import validators
from .model import Jars


class JarForm(FlaskForm):
    jar_name = SelectField("帳戶", choices=Jars.names())


class AbstractIncomeAndExpenseForm(FlaskForm):
    date = DateField('日期', default=datetime.today(),
                     format="%Y-%m-%d",
                     validators=[DataRequired()])
    money = IntegerField('金額', default=0, validators=[
        validators.NumberRange(min=1),

        DataRequired()])

    remark = TextAreaField('備註', validators=[validators.Length(0, 50)])


class AutomaticDistributionIncomeForm(AbstractIncomeAndExpenseForm):
    submit = SubmitField('自動分配收入')


class ManuallyDistributeIncomeForm(JarForm, AbstractIncomeAndExpenseForm):
    submit = SubmitField('手動分配收入')


class ManuallyDistributeExpenseForm(JarForm, AbstractIncomeAndExpenseForm):
    submit = SubmitField('支出')
