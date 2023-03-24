from flask_apispec import MethodResource, use_kwargs, marshal_with, doc
import time
from ...utils import ResponseTool, DecoratorTool, JwtTool, SchemaTool, RedisTool, CustomizeError
from ...six_jar.control import IncomeAndExpenseControl
from .schema import \
    IncomeAndExpenseSchema, \
    ResponseIncomeAndExpenseSchema, \
    DeleteResponseIncomeAndExpenseSchema, \
    RequestIncomeAndExpenseSchema, \
    UserIdSchema

from ... import redis


class AbstractIncomeAndExpense(MethodResource):
    tags_list = ["IncomeAndExpense💰"]
    pass


class IncomeAndExpensePostApi(AbstractIncomeAndExpense):

    @DecoratorTool.integrate(
        tags_list=AbstractIncomeAndExpense.tags_list,
        request_schema=RequestIncomeAndExpenseSchema,
        response_schema=ResponseIncomeAndExpenseSchema)
    def post(self, **kwargs):
        control = IncomeAndExpenseControl(**kwargs)
        control.insert()
        RedisTool.update_user_version(kwargs['user_id'])
        return ResponseTool.result(code=201, message="成功新增", data=control.response_data)

class IncomeAndExpenseApi(AbstractIncomeAndExpense):

    @DecoratorTool.integrate(
        tags_list=AbstractIncomeAndExpense.tags_list,
        request_schema=UserIdSchema,
        response_schema=ResponseIncomeAndExpenseSchema,
        method="GET")
    def get(self, income_and_expense_id, **kwargs):
        control = IncomeAndExpenseControl(id=income_and_expense_id, **kwargs)
        control.read()
        return ResponseTool.success(message="查詢成功", data=control.response_data)

    @DecoratorTool.integrate(
        tags_list=AbstractIncomeAndExpense.tags_list,
        request_schema=RequestIncomeAndExpenseSchema,
        response_schema=ResponseIncomeAndExpenseSchema)
    def put(self, income_and_expense_id, **kwargs):
        control = IncomeAndExpenseControl(id=income_and_expense_id, **kwargs)
        control.update()
        RedisTool.update_user_version(kwargs['user_id'])
        print("put")
        print(control.response_data)
        return ResponseTool.success(message="更新成功", data=control.response_data)

    @DecoratorTool.integrate(
        tags_list=AbstractIncomeAndExpense.tags_list,
        request_schema=UserIdSchema,
        response_schema=DeleteResponseIncomeAndExpenseSchema,
        fresh=True)
    def delete(self, income_and_expense_id, **kwargs):
        control = IncomeAndExpenseControl(id=income_and_expense_id, **kwargs)
        control.delete()
        RedisTool.update_user_version(kwargs['user_id'])
        return ResponseTool.success(message="刪除成功", data=control.response_data)
