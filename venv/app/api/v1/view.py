import time

from marshmallow import Schema, fields
from werkzeug.exceptions import HTTPException
from flask import make_response, copy_current_request_context
from flask_login import login_user
from flask_apispec import MethodResource, use_kwargs, marshal_with, doc
from flask_jwt_extended import \
    jwt_required, current_user, get_jwt_identity, create_access_token, set_access_cookies
from threading import Thread
from . import api_bp, api
from ... import jwt, docs, executor, db, FlaskApp, socketio
from ...utils import ResponseTool, DecoratorTool, JwtTool, SchemaTool, CustomizeError
from ...user.control import UserControl
from ...user.model import User
from ...six_jar.control import IncomeAndExpenseControl
from .schema import \
    EmptySchema, \
    UserRegisterSchema, \
    UserLoginSchema, \
    UserPutSchema, \
    IncomeAndExpenseSchema, \
    UserIdSchema, \
    UserInfoSchema, \
    ResponseIncomeAndExpenseSchema, \
    DeleteResponseIncomeAndExpenseSchema, \
    QueryListIncomeAndExpenseSchema, \
    QueryChartIncomeAndExpenseSchema, \
    RequestIncomeAndExpenseSchema, \
    ChartSchema, \
    FakeDataSchema


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    return ResponseTool.params_error(message=f"重要操作，請輸入密碼")

#
@api_bp.errorhandler(CustomizeError)
def customize_error(e):
    print("api customize_error")
    return ResponseTool.params_error(message=f"失敗,{e}")


# @api_bp.app_errorhandler(Exception)
# def handle_exception(e):
#     # pass through HTTP errors
#     print("api handle_exception")
#     if isinstance(e, HTTPException):
#         return e
#
#     print(e)
#     return ResponseTool.inside_error(message=f"失敗,內部邏輯錯誤")


class AbstractIncomeAndExpense(MethodResource):
    tags_list = ["IncomeAndExpense💰"]
    pass


class AbstractToken(MethodResource):
    tags_list = ["Token"]
    pass


class AbstractUser(MethodResource):
    tags_list = ["User😀"]
    pass


class IncomeAndExpenseListApi(AbstractIncomeAndExpense):
    @DecoratorTool.integrate(
        tags_list=AbstractIncomeAndExpense.tags_list,
        request_schema=QueryListIncomeAndExpenseSchema,
        response_schema=ResponseIncomeAndExpenseSchema,
        return_list=True,
        method="GET")
    def get(self, **kwargs):
        control = IncomeAndExpenseControl(**kwargs)
        income_and_expense_list, total = control.query_list()
        return {"code": "200", "message": "查詢成功", "data": income_and_expense_list, "total": total}


class IncomeAndExpenseChartApi(AbstractIncomeAndExpense):

    @DecoratorTool.integrate(
        tags_list=AbstractIncomeAndExpense.tags_list,
        request_schema=QueryChartIncomeAndExpenseSchema,
        response_schema=ChartSchema,
        method="GET")
    def get(self, **kwargs):
        control = IncomeAndExpenseControl(**kwargs)
        chart_json_str = control.query_chart()
        return ResponseTool.success(message="查詢成功", data={"chart": chart_json_str})


class IncomeAndExpensePostApi(AbstractIncomeAndExpense):

    @DecoratorTool.integrate(
        tags_list=AbstractIncomeAndExpense.tags_list,
        request_schema=RequestIncomeAndExpenseSchema,
        response_schema=ResponseIncomeAndExpenseSchema)
    def post(self, **kwargs):
        control = IncomeAndExpenseControl(**kwargs)
        control.insert()
        return ResponseTool.result(code=201, message="成功新增", data=control.response_data)


class IncomeAndExpenseFakeApi(AbstractIncomeAndExpense):
    @DecoratorTool.integrate(
        tags_list=AbstractIncomeAndExpense.tags_list,
        request_schema=FakeDataSchema,
        response_schema=EmptySchema)
    def post(self, **kwargs):
        number = kwargs["number"]
        control = IncomeAndExpenseControl(**kwargs)

        @copy_current_request_context
        def insert_fake_data(control_object, __number):
            """
            用copy_current_request_context 將當前的app request 上下文,db複製到另一個thread，
            省去app.app_context() 和 其他globe的傳參
            """
            try:
                control_object.insert_fake_data()
                time.sleep(1)
                #flash 是到flask 的session 做寫入，就算成功帶過來thread,下一個request也被無法到這邊取出
                socketio.send(f"新增{__number}筆成功")  # 建立socket雙向連線
            except Exception as e:
                socketio.send(f"新增失敗，請洽資訊人員")
            print("結束新增")

        executor.submit(insert_fake_data, control, number)
        return ResponseTool.result(code=201, message="已在後台，開始新增資料，有結果將回傳通知")


    @DecoratorTool.integrate(
        tags_list=AbstractIncomeAndExpense.tags_list,
        request_schema=UserIdSchema,
        response_schema=EmptySchema)
    def delete(self, **kwargs):
        control = IncomeAndExpenseControl(**kwargs)
        control.delete_fake_data()
        return ResponseTool.success(message="刪除成功")


class IncomeAndExpenseApi(AbstractIncomeAndExpense):

    @DecoratorTool.integrate(
        tags_list=AbstractIncomeAndExpense.tags_list,
        request_schema=UserIdSchema,
        response_schema=ResponseIncomeAndExpenseSchema,
        method="GET")
    def get(self, income_and_expense_id, **kwargs):
        control = IncomeAndExpenseControl(id=income_and_expense_id, **kwargs)
        control.read()
        return ResponseTool.success(message="查詢成功", data=control.response_data)

    @DecoratorTool.integrate(
        tags_list=AbstractIncomeAndExpense.tags_list,
        request_schema=RequestIncomeAndExpenseSchema,
        response_schema=ResponseIncomeAndExpenseSchema)
    def put(self, income_and_expense_id, **kwargs):
        control = IncomeAndExpenseControl(id=income_and_expense_id, **kwargs)
        control.update()
        return ResponseTool.success(message="更新成功", data=control.response_data)

    @DecoratorTool.integrate(
        tags_list=AbstractIncomeAndExpense.tags_list,
        request_schema=UserIdSchema,
        response_schema=DeleteResponseIncomeAndExpenseSchema,
        fresh=True)
    def delete(self, income_and_expense_id, **kwargs):
        control = IncomeAndExpenseControl(id=income_and_expense_id, **kwargs)
        control.delete()
        return ResponseTool.success(message="刪除成功", data=control.response_data)


class TokenRefreshApi(AbstractToken):
    @DecoratorTool.integrate(
        tags_list=AbstractToken.tags_list,
        request_schema=EmptySchema,
        response_schema=EmptySchema,
        refresh=True,
        verify_user=False)
    def post(self):
        user_id = get_jwt_identity()
        resp = make_response(ResponseTool.success(message="token 更新成功"), 302)
        access_token = create_access_token(identity=user_id, fresh=False)
        set_access_cookies(resp, access_token)
        return resp


class UserLoginApi(AbstractToken):

    @doc(tags=AbstractToken.tags_list)
    @use_kwargs(UserLoginSchema, location='json')
    @marshal_with(SchemaTool.return_response_schema(UserIdSchema))
    def post(self, **kwargs):
        control = UserControl()
        resp = control.login(kwargs["email"],
                             kwargs["password"],
                             kwargs["remember_me"],
                             lambda user_id: make_response(
                                 ResponseTool.success(message="登入成功", data={"user_id": user_id}))
                             )
        return resp


class UserLogoutApi(AbstractToken):

    @doc(tags=AbstractToken.tags_list)
    def get(self, **kwargs):
        resp = make_response(ResponseTool.success(message="登出成功", data=kwargs))
        control = UserControl()
        control.logout(resp)
        return resp


class UserPostApi(AbstractUser):

    @doc(tags=AbstractUser.tags_list)
    @use_kwargs(UserRegisterSchema, location='json')
    @marshal_with(SchemaTool.return_response_schema(UserIdSchema))
    def post(self, **kwargs):
        control = UserControl()
        control.register(
            kwargs["email"],
            kwargs["name"],
            kwargs["password"]
        )
        return ResponseTool.result(code=201, message="成功新增", data={"user_id": control.user_id})


class UserApi(AbstractUser):

    @DecoratorTool.integrate(
        tags_list=AbstractUser.tags_list,
        request_schema=EmptySchema,
        response_schema=UserInfoSchema,
        method='GET')
    def get(self, user_id, **kwargs):  # 本來網址就會帶user_id傳給 verify_user_id_and_jwt_cookie
        return ResponseTool.success(message="查詢成功",
                                    data={
                                        "email": current_user.email,
                                        "name": current_user.name})

    @DecoratorTool.integrate(
        tags_list=AbstractUser.tags_list,
        request_schema=UserPutSchema,
        response_schema=UserPutSchema)
    def put(self, user_id, **kwargs):
        control = UserControl()
        is_success = control.change_info(
            user_id,
            kwargs["name"],
            kwargs["password"])
        if is_success:
            return ResponseTool.success(message="修改成功", data=kwargs)
        else:
            return ResponseTool.params_error(message="修改失敗", data=kwargs)

    @DecoratorTool.integrate(
        tags_list=AbstractUser.tags_list,
        request_schema=EmptySchema,
        response_schema=UserIdSchema)
    def delete(self, user_id, **kwargs):
        control = UserControl()
        is_success = control.delete_info(user_id)
        if is_success:
            return ResponseTool.success(message="刪除成功", data={"user_id": user_id})
        else:
            return ResponseTool.params_error(message="刪除失敗", data=kwargs)


api_dict = {
    "/users": UserPostApi,
    "/users/<int:user_id>": UserApi,
    "/users/login": UserLoginApi,
    "/users/logout": UserLogoutApi,
    "/token/refresh": TokenRefreshApi,
    "/income-and-expense": IncomeAndExpensePostApi,
    "/income-and-expense/<int:income_and_expense_id>": IncomeAndExpenseApi,
    "/income-and-expense/fake-data": IncomeAndExpenseFakeApi,
    "/income-and-expense/list": IncomeAndExpenseListApi,
    "/income-and-expense/chart": IncomeAndExpenseChartApi,
}

for route, api_resource in api_dict.items():
    api.add_resource(api_resource, route)
    docs.register(api_resource, blueprint=api_bp.name)
