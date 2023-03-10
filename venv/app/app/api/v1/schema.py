import warnings
from datetime import datetime
from marshmallow import \
    Schema, fields, validates, validate, ValidationError, validates_schema

from ...six_jar.model import Jars
from ...user.model import User

warnings.filterwarnings(
    "ignore",
    message="Multiple schemas resolved to the name "
)

# 錯誤訊息統一
fields.Field.default_error_messages = dict(required="缺少必要參數", type="數據類型錯誤", null="數據不能為空",
                                           validator_failed="驗證錯誤")


class EmptySchema(Schema):
    pass


class ChartSchema(Schema):
    chart = fields.Str(required=True)


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


class TaskIdSchema(Schema):
    task_id = fields.Str(required=True)


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


class IncomeAndExpenseSchema:
    income_and_expense = fields.Str(required=True, validate=validate.OneOf(["income", "expense"]))
    money = fields.Int(required=True, validate=validate.Range(min=1))
    date = fields.DateTime(required=True, format='%Y-%m-%d')
    jar_name = fields.Str(required=True, validate=validate.OneOf(Jars.names()))
    remark = fields.Str(validate=validate.Length(max=50, error='請介於0~50字'))


class RequestIncomeAndExpenseSchema(IncomeAndExpenseSchema, UserIdSchema):
    pass


class ResponseIncomeAndExpenseSchema(IncomeAndExpenseIDSchema, IncomeAndExpenseSchema):
    pass



class QueryConditionIncomeAndExpenseSchema(UserIdSchema):
    sortOrder = fields.Str(validate=validate.OneOf(["asc", "desc"]))
    income_and_expense = fields.Str(validate=validate.OneOf(["income", "expense"]))
    jar_name = fields.Str(validate=validate.OneOf(Jars.names()))
    minimum_money = fields.Int(validate=validate.Range(min=1), load_default=1)
    maximum_money = fields.Int(validate=validate.Range(min=1), load_default=9999)
    earliest_date = fields.Date(format='%Y-%m-%d', load_default=datetime.strptime('2000-01-01', '%Y-%m-%d').date())
    latest_date = fields.Date(format='%Y-%m-%d', load_default=datetime.now().date())

    @validates_schema
    def validate_money(self, data, **kwargs):  # 一定要kwargs
        if data.get("minimum_money") is None:
            return
        if data.get("maximum_money") is None:
            return
        if data["minimum_money"] > data["maximum_money"]:
            raise ValidationError("最小金額>最大金額")

    @validates_schema
    def validate_date(self, data, **kwargs):  # 一定要kwargs
        if data.get("earliest_date") is None:
            return
        if data.get("latest_date") is None:
            return
        if data["earliest_date"] > data["latest_date"]:
            raise ValidationError("最早日期>最晚日期")


class FakeDataSchema(QueryConditionIncomeAndExpenseSchema):
    number = fields.Int(required=True, validate=validate.Range(min=5000, max=1000000))


class QueryListIncomeAndExpenseSchema(QueryConditionIncomeAndExpenseSchema):
    limit = fields.Int(required=True, validate=validate.Range(min=1))
    page = fields.Int(required=True, validate=validate.Range(min=1))
    sort = fields.Str(validate=validate.OneOf(["date", "money", "jar_name"]))


class QueryChartIncomeAndExpenseSchema(QueryConditionIncomeAndExpenseSchema):
    chart_type = fields.Str(required=True, validate=validate.OneOf(["圓餅", "長條", "折線", "直方", "散佈"]))


class DeleteResponseIncomeAndExpenseSchema(IncomeAndExpenseIDSchema, UserIdSchema):
    pass
