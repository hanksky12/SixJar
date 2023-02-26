from marshmallow import Schema, fields
from flask import flash
from flask_apispec import use_kwargs, marshal_with, doc
from flask_jwt_extended import \
    create_access_token, \
    create_refresh_token, \
    set_access_cookies, \
    set_refresh_cookies, \
    unset_jwt_cookies,\
    jwt_required, \
    current_user


def flash_form_error(form):
    for error in form.errors.values():
        flash(error, category='danger')


class JwtTool:
    @staticmethod
    def setting_cookie(resp, user):
        access_token = create_access_token(identity=user, fresh=True)
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
    def inside_error(cls, message="", data=None):
        return cls.result(code=500, message=message, data=data)

    @classmethod
    def result(cls, code, message="", data=None):
        return {"code": code, "message": message, "data": data}


class DecoratorTool:
    @staticmethod
    def integrate(tags_list,
                  request_schema,
                  response_schema,
                  return_list=False,
                  fresh=False,
                  refresh=False,
                  verify_user=True,
                  method='other'
                  ):
        """
        tags_list:  apidoc tag
        request_schema: check input condition
        response_schema: filter output condition
        method: input arg location
        fresh: check jwt_token is fresh
        refresh: check jwt_refresh_token in request
        verify_user: check user_id in (body or query)  is equal to jwt_token or not
        """

        def outer_wrapper(f):
            @doc(tags=tags_list)
            @use_kwargs(request_schema, location=("querystring" if method == "GET" else 'json'))  # 需求的篩選與驗證 失敗就不會進到期下路由
            @marshal_with(SchemaTool.return_response_schema(response_schema, return_list))
            @jwt_required(fresh=fresh, refresh=refresh)
            def wrapper(*args, **kwargs):
                if verify_user and current_user.id != kwargs["user_id"]:
                    return ResponseTool.params_error(message="使用者id驗證不符合cookie", data=kwargs)
                return f(*args, **kwargs)

            return wrapper

        return outer_wrapper


class SchemaTool:
    @staticmethod
    def return_response_schema(schema, return_list=False):
        """
        return_list:  return schema is list or not
        """
        return Schema.from_dict({
            "code": fields.Int(),
            "message": fields.Str(),
            "total": fields.Int(),
            "data": fields.List(fields.Nested(schema)) if return_list else fields.Nested(schema)
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
