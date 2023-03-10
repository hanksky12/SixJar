from flask_apispec import MethodResource, use_kwargs, marshal_with, doc
from flask_jwt_extended import current_user

from ...utils import ResponseTool, DecoratorTool, JwtTool, SchemaTool, CustomizeError
from ...user.control import UserControl
from .schema import \
    EmptySchema, \
    UserRegisterSchema, \
    UserPutSchema, \
    UserIdSchema, \
    UserInfoSchema


class AbstractUser(MethodResource):
    tags_list = ["User😀"]
    pass


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

