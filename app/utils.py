from marshmallow import Schema, fields
from flask import flash
from flask_jwt_extended import \
    create_access_token, \
    create_refresh_token, \
    set_access_cookies, \
    set_refresh_cookies, \
    unset_jwt_cookies
from flask_apispec import use_kwargs, marshal_with, doc
from flask_jwt_extended import jwt_required, current_user


def flash_form_error(form):
    for error in form.errors.values():
        flash(error, category='danger')


class JwtTool:
    @staticmethod
    def setting_cookie(resp, user):
        access_token = create_access_token(identity=user)
        refresh_token = create_refresh_token(identity=user)
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)

    @staticmethod
    def unset_cookie(resp):
        unset_jwt_cookies(resp)


class ResponseTool:
    @classmethod
    def success(cls, message="", data=None):
        return cls.result(200, message, data)

    @classmethod
    def params_error(cls, message="", data=None):
        return cls.result(code=400, message=message, data=data)

    @classmethod
    def result(cls, code, message="", data=None):
        return {"code": code, "message": message, "data": data}


class DecoratorTool:
    @staticmethod
    def integrate(tags_list, request_schema, response_schema):
        def outer_wrapper(f):
            @doc(tags=tags_list)
            @use_kwargs(request_schema, location='json')  # 需求的篩選與驗證 失敗就不會進到期下路由
            @marshal_with(SchemaTool.return_response_schema(response_schema))
            def wrapper(*args, **kwargs):
                return f(*args, **kwargs)

            return wrapper

        return outer_wrapper

    @staticmethod
    def integrate_repeat(tags_list, schema):
        def outer_wrapper(f):
            @DecoratorTool.integrate(tags_list, schema, schema)
            def wrapper(*args, **kwargs):
                return f(*args, **kwargs)

            return wrapper

        return outer_wrapper

    @staticmethod
    def verify_user_id_and_jwt_cookie(f):
        @jwt_required()
        def wrapper(*args, **kwargs):
            if current_user.id != kwargs["user_id"]:
                return ResponseTool.params_error(message="使用者id驗證不符合cookie", data=kwargs)
            return f(*args, **kwargs)

        return wrapper


class SchemaTool:
    @staticmethod
    def return_response_schema(otherschema):
        return Schema.from_dict({
            "code": fields.Int(),
            "message": fields.Str(),
            "data": fields.Nested(otherschema)
        })

    @staticmethod
    def return_response_schema_list(otherschema):
        return Schema.from_dict({
            "code": fields.Int(),
            "message": fields.Str(),
            "data": fields.List(fields.Nested(otherschema))
        })




class CustomizeError(Exception):
    def __init__(self, value, value2="", value3="", value4=""):
        self.value = value
        self.value2 = value2
        self.value3 = value3
        self.value4 = value4

    @classmethod
    def no_record_find(cls):
        return cls("找不到紀錄!!")

    @classmethod
    def no_record_find_or_number_unusual(cls):
        return cls("找不到紀錄或數目異常!!")

    def __str__(self):
        return repr(self.value + self.value2 + self.value3 + self.value4)
