
from flask import render_template
from flask_jwt_extended import \
    create_access_token, \
    create_refresh_token, \
    set_access_cookies, \
    set_refresh_cookies,get_jwt,jwt_required

from . import main_bp
from .. import db


from webargs.flaskparser import  parser, abort

@parser.error_handler
def handle_request_parsing_error(err, req, schema, error_status_code, error_headers):
    """webargs error handler that uses Flask-RESTful's abort function to return
    a JSON error response to the client.
    """
    status_code = error_status_code or 400
    abort(status_code, errors=err.messages)



@main_bp.app_errorhandler(404)
def page_not_found(err):
    return render_template('main/404.html'),404


@main_bp.app_errorhandler(500)
def internal_server_error(err):
    return render_template('main/500.html'),500

@main_bp.route('/')
def index():
    return render_template('main/index.html')

# @jwt_required
# @main_bp.after_request
# def refresh_expiring_jwts(response):
#     try:
#         exp_timestamp = get_jwt()["exp"]
#         now = datetime.now(timezone.utc)
#         target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
#         if target_timestamp > exp_timestamp:
#             access_token = create_access_token(identity=get_jwt_identity())
#             set_access_cookies(response, access_token)
#         return response
#     except (RuntimeError, KeyError):
#         # Case where there is not a valid JWT. Just return the original response
#         return response