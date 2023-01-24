from flask import render_template, flash, request, flash, redirect, url_for
from flask_jwt_extended import unset_jwt_cookies, jwt_required, get_jwt_identity
from flask_login import login_user, current_user, login_required, logout_user

from . import user_bp
from .form import LoginForm, RegisterForm, UserInfoForm
from .control import UserControl
from ..utils import flash_form_error, JwtTool
from .model import User
from .. import db, jwt, login_manager


@user_bp.route("/login2", methods=["POST", "GET"])
def login3():
    form = LoginForm()
    basic_template = "user/login4.html"
    if request.method == "GET":
        return render_template(basic_template, form=form)
    if form.validate_on_submit() is False:
        flash_form_error(form)
        return render_template(basic_template, form=form)
    control = UserControl()
    is_login = control.login(form.email.data,
                             form.password.data)
    if is_login:
        flash("登入成功", category='info')
        resp = redirect(url_for('six_jar.savings'))
        JwtTool.setting_cookie(resp, control.user.id)
        login_user(control.user, form.remember_me.data)
        return resp
    else:
        flash("登入失敗,沒有使用者或密碼錯誤", category='danger')
        return redirect(url_for('user.login3'))


@user_bp.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    basic_template = "user/register.html"
    if request.method == "GET":
        return render_template(basic_template, form=form)
    if form.validate_on_submit() is False:
        flash_form_error(form)
        return render_template(basic_template, form=form)
    control = UserControl()
    control.register(
        form.email.data,
        form.name.data,
        form.password.data
    )
    flash("註冊成功", category='info')
    return redirect(url_for('user.login3'))


@user_bp.route("/user_info", methods=["POST", "GET"])
@login_required
def user_info():
    form = UserInfoForm()
    basic_template = "user/info.html"
    if request.method == "GET":
        form.name.data = current_user.name
        return render_template(basic_template, form=form)
    if form.validate_on_submit() is False:
        flash_form_error(form)
        return render_template(basic_template, form=form)

    control = UserControl()
    is_success = control.change_info(current_user.id, form.name.data, form.password.data)
    if is_success:
        flash("修改成功", category='info')
    else:
        flash("修改失敗", category='danger')
    return redirect(url_for('user.user_info'))


@user_bp.route("/logout", methods=["GET"])
def logout():
    resp = redirect(url_for('main.index'))
    control = UserControl()
    control.logout(resp)
    return resp


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()
