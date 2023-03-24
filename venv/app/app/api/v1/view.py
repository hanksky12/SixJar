from werkzeug.exceptions import HTTPException

from . import api_bp, api
from ...utils import ResponseTool, DecoratorTool, CustomizeError
from ... import jwt
from ...user.model import User



@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    return ResponseTool.params_error(message=f"重要操作，請輸入密碼")


@api_bp.errorhandler(CustomizeError)
def customize_error(e):
    print("view api customize_error")
    return ResponseTool.params_error(message=f"失敗,{e}")


@api_bp.app_errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    print("view api handle_exception")
    if isinstance(e, HTTPException):
        return e

    print(e)
    return ResponseTool.inside_error(message=f"失敗,內部邏輯錯誤")

