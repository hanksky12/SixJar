from flask_apispec import MethodResource, use_kwargs, marshal_with, doc
from flask_jwt_extended import current_user, get_jwt_identity, create_access_token, set_access_cookies
from flask import make_response

from ...utils import ResponseTool, DecoratorTool, JwtTool, SchemaTool, CustomizeError
from ...user.control import UserControl
from .schema import \
    EmptySchema, \
    UserLoginSchema, \
    UserIdSchema


class AbstractToken(MethodResource):
    tags_list = ["Tokenπ"]
    pass


class TokenRefreshApi(AbstractToken):
    @DecoratorTool.integrate(
        tags_list=AbstractToken.tags_list,
        request_schema=EmptySchema,
        response_schema=EmptySchema,
        refresh=True,
        verify_user=False)
    def post(self):
        user_id = get_jwt_identity()
        resp = make_response(ResponseTool.success(message="token ζ΄ζ°ζε"), 302)
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
                                 ResponseTool.success(message="η»ε₯ζε", data={"user_id": user_id}))
                             )
        return resp


class UserLogoutApi(AbstractToken):

    @doc(tags=AbstractToken.tags_list)
    def get(self, **kwargs):
        resp = make_response(ResponseTool.success(message="η»εΊζε", data=kwargs))
        control = UserControl()
        control.logout(resp)
        return resp
