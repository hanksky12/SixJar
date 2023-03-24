from flask import render_template, flash, request, redirect, url_for, flash
from datetime import datetime
from flask_login import login_user, current_user, login_required

from .form import AutomaticDistributionIncomeForm, ManuallyDistributeIncomeForm, ManuallyDistributeExpenseForm
from . import six_jar_bp
from .model import Jar, Savings, IncomeAndExpense, Jars
from .control import IncomeAndExpenseControl
from ..utils import flash_form_error, CustomizeError
from .. import cache, redis


@six_jar_bp.route("/expense", methods=["POST", "GET"])
@login_required
def expense():
    form = ManuallyDistributeExpenseForm()
    basic_template = render_template("six_jar/expense.html", form=form)
    if request.method == "GET":
        return basic_template
    if form.validate_on_submit() is False:
        flash_form_error(form)
        return basic_template
    control = IncomeAndExpenseControl(
        user_id=current_user.id,
        income_and_expense="expense",
        money=form.money.data,
        date=form.date.data,
        remark=form.remark.data,
        jar_name=form.jar_name.data
    )
    control.insert()
    flash("新增支出成功", category='info')
    if control.saving < 0:
        flash(f"{form.jar_name.data}已經超支,剩下餘額：{control.saving}", category='warning')
    return redirect(url_for('six_jar.expense'))


@six_jar_bp.route("/income", methods=["POST", "GET"])
@login_required
def income():
    manually_form = ManuallyDistributeIncomeForm()
    automatic_form = AutomaticDistributionIncomeForm()
    basic_template = "six_jar/income.html"
    if request.method == "GET":
        return render_template(basic_template, form=manually_form, form2=automatic_form)
    if manually_form.manu_submit.data and manually_form.validate_on_submit():
        control = IncomeAndExpenseControl(
            user_id=current_user.id,
            income_and_expense="income",
            money=manually_form.money.data,
            date=manually_form.date.data,
            remark=manually_form.remark.data,
            jar_name=manually_form.jar_name.data
        )
        control.insert()
        flash("新增收入成功", category='info')
        return redirect(url_for('six_jar.income'))
    elif automatic_form.auto_submit.data and automatic_form.validate_on_submit():
        control = IncomeAndExpenseControl(
            user_id=current_user.id,
            all_money=manually_form.money.data,
            date=manually_form.date.data,
            remark=manually_form.remark.data,
        )
        control.auto_insert_income()
        for index, money in enumerate(control.distribution_money_list):
            flash(f"「{Jars.names()[index]}」新增: {money}元成功", category='info')
        return redirect(url_for('six_jar.income'))

    else:
        flash_form_error(manually_form)
        flash_form_error(automatic_form)
        return render_template(basic_template, form=manually_form, form2=automatic_form)


@six_jar_bp.route("/savings", methods=["GET"])
@login_required
def savings():
    control = IncomeAndExpenseControl(user_id=current_user.id)
    control.init_savings()
    savings_list, total_savings = control.get_saving_list()
    message = "生活還算過得去^^" if total_savings > 1000 else "請注意開銷～"
    flash(f"帳戶總額：{total_savings}元;  {message}", category='info')
    update_time = redis.get('update_time')

    login_times = redis.get(f'login_times_for_user:{current_user.id}')
    return render_template("six_jar/savings.html",
                           savings_list=savings_list,
                           user_name=current_user.name,
                           exchange_rate_update_time=update_time,
                           login_times=login_times
                           )


@six_jar_bp.route("/income-and-expense-table", methods=["GET"])
@login_required
@cache.cached(timeout=20 * 60)
def income_and_expense_table():
    return render_template("six_jar/income_and_expense_table.html", jar_name=Jars.names(), today=datetime.now().date())


@six_jar_bp.route("/income-and-expense-chart", methods=["GET"])
@login_required
@cache.cached(timeout=20 * 60)
def income_and_expense_chart():
    return render_template("six_jar/income_and_expense_chart.html", jar_name=Jars.names(), today=datetime.now().date())


@six_jar_bp.route("/income-and-expense-fake-data", methods=["GET"])
@login_required
@cache.cached(timeout=20 * 60)
def income_and_expense_fake_data():
    return render_template("six_jar/income_and_expense_fake_data.html", jar_name=Jars.names(), today=datetime.now().date())
