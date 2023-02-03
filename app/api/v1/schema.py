from marshmallow import Schema, fields, validates, validate, ValidationError, validates_schema

from ...six_jar.model import Jars
from ...user.model import User

import warnings

warnings.filterwarnings(
    "ignore",
    message="Multiple schemas resolved to the name "
)

# 錯誤訊息統一
fields.Field.default_error_messages = dict(required="缺少必要參數", type="數據類型錯誤", null="數據不能為空",
                                           validator_failed="驗證錯誤")


class EmptySchema(Schema):
    pass


class EmailSchema(Schema):
    email = fields.Str(required=True, validate=validate.Length(1, 50, error='信箱長度請於1-50字'))


class PasswordSchema(Schema):
    password = fields.Str(required=True, validate=validate.Length(2, 10, error='密碼長度請於2-10字'))


class UserNameSchema(Schema):
    name = fields.Str(required=True)


class UserInfoSchema(EmailSchema, UserNameSchema):
    pass


class UserLoginSchema(EmailSchema, PasswordSchema):
    remember_me = fields.Bool(required=True)


class UserIdSchema(Schema):
    user_id = fields.Int(required=True)


class UserPutSchema(UserNameSchema, PasswordSchema):
    password2 = fields.Str(required=True)

    @validates_schema
    def validate_password2(self, data, **kwargs):  # 一定要kwargs
        if data["password"] != data["password2"]:
            raise ValidationError("兩次密碼不相等")


class UserRegisterSchema(EmailSchema, UserPutSchema):
    @validates("email")
    def validate_email(self, value):
        if User.query.filter_by(email=value).first():
            raise ValidationError('Mail已被註冊')


class IncomeAndExpenseIDSchema(Schema):
    id = fields.Int(required=True)


class IncomeAndExpenseSchema():
    income_and_expense = fields.Str(required=True, validate=validate.OneOf(["income", "expense"]))
    money = fields.Int(required=True, validate=validate.Range(min=1))
    date = fields.DateTime(required=True, format='%Y-%m-%d')
    jar_name = fields.Str(required=True, validate=validate.OneOf(Jars.names()))
    remark = fields.Str(validate=validate.Length(max=50, error='請介於0~50字'))


class RequestIncomeAndExpenseSchema(IncomeAndExpenseSchema,UserIdSchema):
    pass


class ResponseIncomeAndExpenseSchema(IncomeAndExpenseIDSchema, IncomeAndExpenseSchema):
    pass


class QueryIncomeAndExpenseSchema(Schema):
    user_id = fields.Int(required=True)
    limit = fields.Int(required=True, validate=validate.Range(min=1))
    page = fields.Int(required=True, validate=validate.Range(min=1))
    sortOrder = fields.Str(required=True, validate=validate.OneOf(["asc", "desc"]))
    sort = fields.Str(validate=validate.OneOf(["date", "money", "jar_name"]))
    income_and_expense = fields.Str(validate=validate.OneOf(["income", "expense"]))
    jar_name = fields.Str(validate=validate.OneOf(Jars.names()))
    minimum_money = fields.Int(validate=validate.Range(min=1))
    maximum_money = fields.Int(validate=validate.Range(min=1))
    earliest_date = fields.DateTime(format='%Y-%m-%d')
    latest_date = fields.DateTime(format='%Y-%m-%d')



class DeleteResponseIncomeAndExpenseSchema(IncomeAndExpenseIDSchema, UserIdSchema):
    pass
