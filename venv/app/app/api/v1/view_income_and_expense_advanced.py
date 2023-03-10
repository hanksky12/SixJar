from flask_apispec import MethodResource, use_kwargs, marshal_with, doc
from ... import celery
from ...utils import ResponseTool, DecoratorTool, JwtTool, SchemaTool, CustomizeError
from ...six_jar.control import IncomeAndExpenseControl
from .schema import \
    EmptySchema, \
    ResponseIncomeAndExpenseSchema, \
    QueryListIncomeAndExpenseSchema, \
    QueryChartIncomeAndExpenseSchema, \
    UserIdSchema, \
    ChartSchema, \
    FakeDataSchema, \
    TaskIdSchema


class AbstractIncomeAndExpenseAdvanced(MethodResource):
    tags_list = ["IncomeAndExpenseAdvanced💸"]
    pass


class IncomeAndExpenseListApi(AbstractIncomeAndExpenseAdvanced):
    @DecoratorTool.integrate(
        tags_list=AbstractIncomeAndExpenseAdvanced.tags_list,
        request_schema=QueryListIncomeAndExpenseSchema,
        response_schema=ResponseIncomeAndExpenseSchema,
        return_list=True,
        method="GET")
    def get(self, **kwargs):
        control = IncomeAndExpenseControl(**kwargs)
        income_and_expense_list, total = control.query_list()
        return {"code": "200", "message": "查詢成功", "data": income_and_expense_list, "total": total}


class IncomeAndExpenseChartApi(AbstractIncomeAndExpenseAdvanced):

    @DecoratorTool.integrate(
        tags_list=AbstractIncomeAndExpenseAdvanced.tags_list,
        request_schema=QueryChartIncomeAndExpenseSchema,
        response_schema=ChartSchema,
        method="GET")
    def get(self, **kwargs):
        control = IncomeAndExpenseControl(**kwargs)
        chart_json_str = control.query_chart()
        return ResponseTool.success(message="查詢成功", data={"chart": chart_json_str})


class IncomeAndExpenseFakeApi(AbstractIncomeAndExpenseAdvanced):
    """
    case1:開線程＋websocket
        control = IncomeAndExpenseControl(**kwargs)
        @copy_current_request_context
        def insert_fake_data(control_object, __number):
            #用copy_current_request_context 將當前的app request 上下文,db複製到另一個thread，
            #省去app.app_context() 和 其他globe的傳參
            try:
                control_object.insert_fake_data()
                time.sleep(1)
                #flash 是到flask 的session 做寫入，就算成功帶過來thread,下一個request也被無法到這邊取出
                socketio.send(f"新增{__number}筆成功")  # 建立socket雙向連線
            except Exception as e:
                print(e)
                socketio.send(f"新增失敗，請洽資訊人員")
            print("結束新增")
        executor.submit(insert_fake_data, control, number)
        return ResponseTool.result(code=201, message="已在後台，開始新增資料，有結果將回傳通知")

    case2:使用 celery worker＋sse
    """

    @DecoratorTool.integrate(
        tags_list=AbstractIncomeAndExpenseAdvanced.tags_list,
        request_schema=FakeDataSchema,
        response_schema=TaskIdSchema)
    def post(self, **kwargs):
        task = celery.send_task(name='insert_fake_data', kwargs=kwargs)
        return ResponseTool.result(code=202,
                                   message="已在後台，開始操作資料，有結果將回傳通知",
                                   data={"task_id": task.id})

    @DecoratorTool.integrate(
        tags_list=AbstractIncomeAndExpenseAdvanced.tags_list,
        request_schema=UserIdSchema,
        response_schema=EmptySchema)
    def delete(self, **kwargs):
        control = IncomeAndExpenseControl(**kwargs)
        control.delete_fake_data()
        return ResponseTool.success(message="刪除成功")
