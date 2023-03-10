from flask import Blueprint
from flask_restful import Api

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

from ... import docs
from . import view
from . import view_user as user
from . import view_task as task
from . import view_token as token
from . import view_income_and_expense as income_and_expense
from . import view_income_and_expense_advanced as income_and_expense_advanced



api_dict = {
    "/users": user.UserPostApi,
    "/users/<int:user_id>": user.UserApi,
    "/users/login": token.UserLoginApi,
    "/users/logout": token.UserLogoutApi,
    "/token/refresh": token.TokenRefreshApi,
    "/income-and-expense": income_and_expense.IncomeAndExpensePostApi,
    "/income-and-expense/<int:income_and_expense_id>": income_and_expense.IncomeAndExpenseApi,
    "/income-and-expense/fake-data": income_and_expense_advanced.IncomeAndExpenseFakeApi,
    "/income-and-expense/list": income_and_expense_advanced.IncomeAndExpenseListApi,
    "/income-and-expense/chart": income_and_expense_advanced.IncomeAndExpenseChartApi,
    '/task/<string:task_id>': task.TaskApi
}

for route, api_resource in api_dict.items():
    api.add_resource(api_resource, route)
    docs.register(api_resource, blueprint=api_bp.name)
