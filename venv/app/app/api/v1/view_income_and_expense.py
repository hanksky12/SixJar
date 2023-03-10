from flask_apispec import MethodResource, use_kwargs, marshal_with, doc

from ...utils import ResponseTool, DecoratorTool, JwtTool, SchemaTool, CustomizeError
from ...six_jar.control import IncomeAndExpenseControl
from .schema import \
    IncomeAndExpenseSchema, \
    ResponseIncomeAndExpenseSchema, \
    DeleteResponseIncomeAndExpenseSchema, \
    RequestIncomeAndExpenseSchema, \
    UserIdSchema


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
        return ResponseTool.success(message="更新成功", data=control.response_data)

    @DecoratorTool.integrate(
        tags_list=AbstractIncomeAndExpense.tags_list,
        request_schema=UserIdSchema,
        response_schema=DeleteResponseIncomeAndExpenseSchema,
        fresh=True)
    def delete(self, income_and_expense_id, **kwargs):
        control = IncomeAndExpenseControl(id=income_and_expense_id, **kwargs)
        control.delete()
        return ResponseTool.success(message="刪除成功", data=control.response_data)
