from marshmallow import Schema, fields
from flask_apispec import MethodResource, use_kwargs, marshal_with, doc
from flask_jwt_extended import jwt_required, current_user, get_jwt_identity, create_access_token, set_access_cookies
from flask import make_response
from flask_login import login_user
from werkzeug.exceptions import HTTPException

from . import api_bp, api
from ...utils import ResponseTool, DecoratorTool, JwtTool, SchemaTool, CustomizeError
from ...user.control import UserControl
from ...user.model import User
from ...six_jar.control import IncomeAndExpenseControl
from ... import jwt, docs
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
    QueryIncomeAndExpenseSchema, \
    RequestIncomeAndExpenseSchema


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()

@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):

    return ResponseTool.params_error(message=f"重大操作，請登入")


class IncomeAndExpenseSearchApi(MethodResource):
    @doc(tags=["IncomeAndExpense💰"])
    @use_kwargs(QueryIncomeAndExpenseSchema(), location='querystring')
    @marshal_with(SchemaTool.return_response_schema_list(ResponseIncomeAndExpenseSchema))
    @DecoratorTool.verify_user_id_and_jwt_cookie()
    def get(self, **kwargs):
        control = IncomeAndExpenseControl(**kwargs)
        income_and_expense_list, total = control.query()
        return {"code": "200", "message": "查詢成功", "data": income_and_expense_list, "total": total}


class IncomeAndExpensePostApi(MethodResource):
    tags_list = ["IncomeAndExpense💰"]

    @DecoratorTool.integrate(tags_list, RequestIncomeAndExpenseSchema, ResponseIncomeAndExpenseSchema)
    @DecoratorTool.verify_user_id_and_jwt_cookie()
    def post(self, **kwargs):
        control = IncomeAndExpenseControl(**kwargs)
        control.insert()
        return ResponseTool.result(code=201, message="成功新增", data=control.response_data)


class IncomeAndExpenseApi(MethodResource):
    tags_list = ["IncomeAndExpense💰"]

    @DecoratorTool.integrate(tags_list, UserIdSchema, ResponseIncomeAndExpenseSchema)
    @DecoratorTool.verify_user_id_and_jwt_cookie()
    def get(self, income_and_expense_id, **kwargs):
        control = IncomeAndExpenseControl(id=income_and_expense_id, **kwargs)
        control.read()
        return ResponseTool.success(message="查詢成功", data=control.response_data)


    @DecoratorTool.integrate(tags_list, RequestIncomeAndExpenseSchema, ResponseIncomeAndExpenseSchema)
    @DecoratorTool.verify_user_id_and_jwt_cookie()
    def put(self, income_and_expense_id, **kwargs):
        control = IncomeAndExpenseControl(id=income_and_expense_id, **kwargs)
        control.update()
        return ResponseTool.success(message="更新成功", data=control.response_data)


    @DecoratorTool.integrate(tags_list, UserIdSchema, DeleteResponseIncomeAndExpenseSchema)
    @DecoratorTool.verify_user_id_and_jwt_cookie(fresh=True)
    def delete(self, income_and_expense_id, **kwargs):
        control = IncomeAndExpenseControl(id=income_and_expense_id, **kwargs)
        control.delete()
        return ResponseTool.success(message="刪除成功", data=control.response_data)



class TokenRefreshApi(MethodResource):
    @DecoratorTool.integrate_repeat(["Token"], EmptySchema)
    @jwt_required(refresh=True)
    def post(self):
        user_id = get_jwt_identity()
        resp = make_response(ResponseTool.success(message="token 更新成功"), 302)
        access_token = create_access_token(identity=user_id, fresh=False)
        set_access_cookies(resp, access_token)
        return resp


class UserLoginApi(MethodResource):
    @DecoratorTool.integrate(["Token"], UserLoginSchema, UserIdSchema)
    def post(self, **kwargs):
        control = UserControl()
        resp = control.login(kwargs["email"],
                             kwargs["password"],
                             kwargs["remember_me"],
                             lambda user_id: make_response(
                                 ResponseTool.success(message="登入成功", data={"user_id": user_id}))
                             )
        return resp


class UserLogoutApi(MethodResource):
    @DecoratorTool.integrate_repeat(["Token"], EmptySchema)
    def get(self, **kwargs):
        resp = make_response(ResponseTool.success(message="登出成功", data=kwargs))
        control = UserControl()
        control.logout(resp)
        return resp


class UserPostApi(MethodResource):
    @DecoratorTool.integrate(["User😀"], UserRegisterSchema, UserIdSchema)
    def post(self, **kwargs):
        control = UserControl()
        control.register(
            kwargs["email"],
            kwargs["name"],
            kwargs["password"]
        )
        return ResponseTool.result(code=201, message="成功新增", data={"user_id": control.user_id})


class UserApi(MethodResource):
    tags_list = ["User😀"]

    @DecoratorTool.integrate(tags_list, EmptySchema, UserInfoSchema)
    @DecoratorTool.verify_user_id_and_jwt_cookie()
    def get(self, user_id, **kwargs):  # 傳給 verify_user_id_and_jwt_cookie
        return ResponseTool.success(message="查詢成功", data={"email": current_user.email,
                                                              "name": current_user.name})

    @DecoratorTool.integrate_repeat(tags_list, UserPutSchema)
    @DecoratorTool.verify_user_id_and_jwt_cookie()
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

    @DecoratorTool.integrate(tags_list, EmptySchema, UserIdSchema)
    @DecoratorTool.verify_user_id_and_jwt_cookie()
    def delete(self, user_id, **kwargs):
        control = UserControl()
        is_success = control.delete_info(user_id)
        if is_success:
            return ResponseTool.success(message="刪除成功", data={"user_id": user_id})
        else:
            return ResponseTool.params_error(message="刪除失敗", data=kwargs)

@api_bp.errorhandler(CustomizeError)
def customizeError(e):
    return ResponseTool.params_error(message=f"失敗,{e}")

@api_bp.app_errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e
    print(e)
    return ResponseTool.inside_error(message=f"失敗,內部邏輯錯誤")


api_dict = {
    "/users": UserPostApi,
    "/users/<int:user_id>": UserApi,
    "/users/login": UserLoginApi,
    "/users/logout": UserLogoutApi,
    "/token/refresh": TokenRefreshApi,
    "/income-and-expense": IncomeAndExpensePostApi,
    "/income-and-expense/search": IncomeAndExpenseSearchApi,
    "/income-and-expense/<int:income_and_expense_id>": IncomeAndExpenseApi,
}

for route, api_resource in api_dict.items():
    api.add_resource(api_resource, route)
    docs.register(api_resource, blueprint=api_bp.name)
