from flask_apispec import MethodResource
from marshmallow import Schema, fields
from flask_apispec import use_kwargs, marshal_with, doc
from flask_jwt_extended import jwt_required, current_user
from flask import make_response
from flask_login import login_user

from . import api_bp, api
from ...utils import ResponseTool, DecoratorTool, JwtTool
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
    DeleteResponseIncomeAndExpenseSchema


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


class IncomeAndExpensePostApi(MethodResource):
    tags_list = ["IncomeAndExpense💰"]

    @DecoratorTool.integrate(tags_list, IncomeAndExpenseSchema, ResponseIncomeAndExpenseSchema)
    @DecoratorTool.verify_user_id_and_jwt_cookie
    def get(self):
        pass

    @DecoratorTool.integrate(tags_list, IncomeAndExpenseSchema, ResponseIncomeAndExpenseSchema)
    @DecoratorTool.verify_user_id_and_jwt_cookie
    def post(self, **kwargs):
        control = IncomeAndExpenseControl(**kwargs)
        control.insert()
        return ResponseTool.result(code=201, message="成功新增", data=control.response_data)


class IncomeAndExpenseApi(MethodResource):
    tags_list = ["IncomeAndExpense💰"]

    @DecoratorTool.integrate(tags_list, UserIdSchema, ResponseIncomeAndExpenseSchema)
    @DecoratorTool.verify_user_id_and_jwt_cookie
    def get(self, income_and_expense_id, **kwargs):
        try:
            control = IncomeAndExpenseControl(income_and_expense_id=income_and_expense_id, **kwargs)
            control.read()
            return ResponseTool.success(message="查詢成功", data=control.response_data)
        except Exception as e:
            return ResponseTool.params_error(message=f"查詢失敗,{e}")

    @DecoratorTool.integrate(tags_list, IncomeAndExpenseSchema, ResponseIncomeAndExpenseSchema)
    @DecoratorTool.verify_user_id_and_jwt_cookie
    def put(self, income_and_expense_id, **kwargs):
        try:
            control = IncomeAndExpenseControl(income_and_expense_id=income_and_expense_id,**kwargs)
            control.update()
            return ResponseTool.success(message="更新成功", data=control.response_data)
        except Exception as e:
            return ResponseTool.params_error(message=f"更新失敗,{e}")


    @DecoratorTool.integrate(tags_list, UserIdSchema, DeleteResponseIncomeAndExpenseSchema)
    @DecoratorTool.verify_user_id_and_jwt_cookie
    def delete(self, income_and_expense_id, **kwargs):
        try:
            control = IncomeAndExpenseControl(income_and_expense_id=income_and_expense_id,**kwargs)
            control.delete()
            return ResponseTool.success(message="刪除成功", data=control.response_data)
        except Exception as e:
            return ResponseTool.params_error(message=f"刪除失敗,{e}")


class TokenRefreshApi(MethodResource):
    @DecoratorTool.integrate_repeat(["Token"], EmptySchema)
    @jwt_required(refresh=True)
    def post(self):
        user_id = get_jwt_identity()
        access_token = create_access_token(identity=user_id)
        resp = make_response(ResponseTool.success(message="token 更新成功"), 302)
        set_access_cookies(resp, access_token)
        return resp


class UserLoginApi(MethodResource):
    @DecoratorTool.integrate(["Token"], UserLoginSchema, UserIdSchema)
    def post(self, **kwargs):
        try:
            control = UserControl()
            control.login(kwargs["email"],
                                     kwargs["password"])
            resp = make_response(ResponseTool.success(message="登入成功", data={"user_id": control.user_id}))
            JwtTool.setting_cookie(resp, control.user.id)
            login_user(control.user, kwargs["remember_me"])
            return resp
        except Exception as e:
            return ResponseTool.params_error(message=f"登入失敗,{e}", data=kwargs)


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
    @DecoratorTool.verify_user_id_and_jwt_cookie
    def get(self, user_id, **kwargs):  # 傳給 verify_user_id_and_jwt_cookie
        return ResponseTool.success(message="查詢成功", data={"email": current_user.email,
                                                              "name": current_user.name})

    @DecoratorTool.integrate_repeat(tags_list, UserPutSchema)
    @DecoratorTool.verify_user_id_and_jwt_cookie
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
    @DecoratorTool.verify_user_id_and_jwt_cookie
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
    "/income_and_expense": IncomeAndExpensePostApi,
    "/income_and_expense/<int:income_and_expense_id>": IncomeAndExpenseApi,
}

for route, api_resource in api_dict.items():
    api.add_resource(api_resource, route)
    docs.register(api_resource, blueprint=api_bp.name)
