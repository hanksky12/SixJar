from flask import render_template, flash, redirect, url_for
from flask_jwt_extended import \
    create_access_token, \
    create_refresh_token, \
    set_access_cookies, \
    set_refresh_cookies,get_jwt,jwt_required

from . import main_bp
from .. import db
from ..utils import CustomizeError

from webargs.flaskparser import  parser, abort
from werkzeug.exceptions import HTTPException



@parser.error_handler
def handle_request_parsing_error(err, req, schema, error_status_code, error_headers):
    """webargs error handler that uses Flask-RESTful's abort function to return
    a JSON error response to the client.
    """
    status_code = error_status_code or 400
    abort(status_code, errors=err.messages)


@main_bp.app_errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e
    print(e)
    flash(f"內部遇到,未知錯誤,請洽資訊人員修正！", category='danger')
    return redirect(url_for('main.index'))

@main_bp.app_errorhandler(CustomizeError)
def customizeError(err):
    flash(f"出錯囉！ {err}", category='danger')
    return redirect(url_for('main.index'))

@main_bp.app_errorhandler(404)
def page_not_found(err):
    return render_template('main/404.html'),404


@main_bp.app_errorhandler(500)
def internal_server_error(err):
    return render_template('main/500.html'),500

@main_bp.route('/')
def index():
    return render_template('main/index.html')
