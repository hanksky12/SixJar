from marshmallow import Schema, fields
import time
import json
from flask import flash, current_app, jsonify
import flask
import pickle
from functools import wraps
from jwt import exceptions
from flask_apispec import use_kwargs, marshal_with, doc
from flask_jwt_extended import \
    create_access_token, \
    create_refresh_token, \
    set_access_cookies, \
    set_refresh_cookies, \
    unset_jwt_cookies, \
    jwt_required, \
    current_user, \
    verify_jwt_in_request
from flask_login import current_user as flask_login_current_user
import urllib.parse
from . import cache, redis


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
    def token_error(cls, message="", data=None):
        return cls.result(code=401, message=message, data=data)

    @classmethod
    def inside_error(cls, message="", data=None):
        return cls.result(code=500, message=message, data=data)

    @classmethod
    def result(cls, code, message="", data=None):
        return {"code": code, "message": message, "data": data}

    @classmethod
    def bad_request(cls, message):
        response = jsonify({'message': message})
        response.status_code = 401
        return response


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
            @DecoratorTool.jwt_required_customized(fresh=fresh, refresh=refresh)
            def wrapper(*args, **kwargs):
                if verify_user and current_user.id != kwargs["user_id"]:
                    return ResponseTool.params_error(message="使用者id驗證不符合cookie", data=kwargs)
                return f(*args, **kwargs)

            return wrapper

        return outer_wrapper

    @staticmethod
    def jwt_required_customized(
            optional=False,
            fresh=False,
            refresh=False,
            locations=None,
            verify_type=True):
        def wrapper(fn):
            @wraps(fn)
            def decorator(*args, **kwargs):
                try:
                    verify_jwt_in_request(optional, fresh, refresh, locations, verify_type)
                    return current_app.ensure_sync(fn)(*args, **kwargs)
                except exceptions.ExpiredSignatureError as e:
                    print("exceptions.ExpiredSignatureError")
                    print(e)
                    return ResponseTool.bad_request(message="Signature has expired")

            return decorator

        return wrapper


class RedisTool:
    @staticmethod
    def update_user_version(user_id):
        print(f"update_user_version: {user_id}")
        redis.set(f"user_id:{user_id}", int(time.time()))

    @staticmethod
    def is_logged_in_for_cache():
        def wrapper(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                def __handle_response(__key):
                    __response = cache.get(__key)
                    if not __response:
                        __response = f(*args, **kwargs)
                        cache.set(__key, __response)
                    return __response

                key = 'logged_in_index' if flask_login_current_user.is_authenticated else 'not_logged_in_index'
                return __handle_response(key)

            return decorated_function

        return wrapper

    @staticmethod
    def cache(prefix="", key_args=None, version_key="user_id", version_args=["user_id"], timeout=60 * 60):
        """
        user version to decide cache is valid or not
        """

        def wrapper(fn):
            @wraps(fn)
            def decorator(*args, **kwargs):
                key = __create_key(kwargs)
                v_key = __create_version_key(kwargs)
                bind_key_version_cache, response_cache = __get_cache_from_redis(key, v_key)
                if response_cache:
                    response, this_time_version = __get_response_and_version_from_cache(response_cache)
                    bind_key_version = int(bind_key_version_cache) if bind_key_version_cache else 0
                    if this_time_version >= bind_key_version:
                        print("get data from cache")
                        return response['data']
                response = fn(*args, **kwargs)
                if response:
                    print(f"set data to cache")
                    response_cached = __set_response_and_version_to_cache(response)
                    redis.setex(key, timeout, response_cached)
                return response

            def __set_response_and_version_to_cache(response):
                response_cached = json.dumps({'data': response, 'version': int(time.time())})
                return response_cached

            def __get_response_and_version_from_cache(response_cache):
                response = json.loads(response_cache)
                return response, response['version']

            def __get_cache_from_redis(key, v_key):
                pipe = redis.pipeline()
                pipe.get(key)
                pipe.get(v_key)
                ret = pipe.execute()
                response = ret[0]
                bind_key_version = ret[1]
                return bind_key_version, response

            def __create_version_key(kwargs):
                v_key = version_key
                for item in version_args:
                    v_key += ":{}".format(kwargs[item])

                print(f"v_key: {v_key}")
                return v_key

            def __create_key(kwargs):
                if key_args is None:
                    key = str(prefix) + flask.request.path + '?' + '&'.join([f"{k}={v}" for k, v in kwargs.items()])
                else:
                    key = str(prefix) + str(key_args)
                print("key:{}".format(key))
                return key

            return decorator

        return wrapper


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
