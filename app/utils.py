
from flask import flash
from flask_jwt_extended import \
    create_access_token, \
    create_refresh_token, \
    set_access_cookies, \
    set_refresh_cookies


def flash_form_error(form):
    for error in form.errors.values():
        flash(error, category='danger')



def setting_jwt_cookie(resp, user):
    access_token = create_access_token(identity=user)
    refresh_token = create_refresh_token(identity=user)
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
