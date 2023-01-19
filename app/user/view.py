from flask import render_template

from . import user_bp
from .form import LoginForm


@user_bp.route("/login2", methods=["POST", "GET"])#路由自訂
def login3():
    form = LoginForm()
    # if form.validate_on_submit():
    #     session['name'] = form.name.data
    #     session['agreed'] = form.agreed.data
    #     session['gender'] = form.gender.data
    #     session['hobby'] = form.hobby.data
    #     session['others'] = form.others.data
    #     return redirect(url_for('thankyou'))
    # else:
    #     # 表單的報錯，密碼兩次相等檢查錯誤會在errors，不會直接顯示，要取出來丟出來
    #     for error in form.errors.values():
    #         flash(error, category='danger')

    return render_template("user/login4.html", form=form)