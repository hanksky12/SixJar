from flask import render_template, flash, request, redirect, url_for, flash
import datetime
from flask_login import login_user, current_user, login_required

from .form import AutomaticDistributionIncomeForm, ManuallyDistributeIncomeForm, ManuallyDistributeExpenseForm
from . import six_jar_bp
from .model import Jar, Savings, IncomeAndExpense
from .control import IncomeAndExpenseControl

@login_required
@six_jar_bp.route("/expense", methods=["POST", "GET"])
def expense():
    form = ManuallyDistributeExpenseForm()
    basic_template = render_template("six_jar/expense.html", form=form)
    if request.method == "GET":
        return basic_template
    if form.validate_on_submit() is False:
        flash_form_error()
        return basic_template
    control = IncomeAndExpenseControl(current_user.id)
    control.add(
        income_and_expense="expense",
        money=form.money.data,
        date=form.date.data,
        remark=form.remark.data,
        jar_name=form.jar_name.data
    )

    flash("新增支出成功", category='info')
    if control.saving<0:
        flash(f"{form.jar_name.data}已經超支,剩下餘額：{control.saving}", category='warning')
    return redirect(url_for('six_jar.expense'))


@login_required
@six_jar_bp.route("/income", methods=["POST", "GET"])
def income():
    manually_form = ManuallyDistributeIncomeForm()
    automatic_form = AutomaticDistributionIncomeForm()
    basic_template = render_template("six_jar/income.html", form=manually_form, form2=automatic_form)
    if request.method == "GET":
        return basic_template
    if manually_form.validate_on_submit() is False or automatic_form.validate_on_submit() is False:
        flash_form_error()
        return basic_template

    if manually_form.validate_on_submit():
        control = IncomeAndExpenseControl(current_user.id)
        control.add(
            income_and_expense="income",
            money=manually_form.money.data,
            date=manually_form.date.data,
            remark=manually_form.remark.data,
            jar_name=manually_form.jar_name.data
        )
        flash("新增收入成功", category='info')
    else:
        pass
    return redirect(url_for('six_jar.income'))

@login_required
@six_jar_bp.route("/savings", methods=["GET"])
def savings():
    control = IncomeAndExpenseControl(current_user.id)
    control.init_savings()
    savings_list = control.get_saving_list()
    return render_template("six_jar/savings.html",
                           savings_list=savings_list,
                           user_name=current_user.name)
