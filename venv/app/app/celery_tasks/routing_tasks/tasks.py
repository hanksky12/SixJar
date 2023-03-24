from datetime import datetime
from ... import celery
from ...extension import FlaskApp
from ...six_jar.control import IncomeAndExpenseControl
from ...user.model import User  # 不import worker讀不到
from ..utils import update_task_status


@celery.task(name="insert_fake_data", bind=True)  # bind 可在任務裡更新狀態，用self傳遞
def insert_fake_data(self, **kwargs):
    update_status = update_task_status(self)
    # 因序列化後要轉換回去
    kwargs["earliest_date"] = datetime.strptime(kwargs["earliest_date"], '%Y-%m-%dT%H:%M:%S').date()
    kwargs["latest_date"] = datetime.strptime(kwargs["latest_date"], '%Y-%m-%dT%H:%M:%S').date()

    with FlaskApp().app.app_context():
        control = IncomeAndExpenseControl(**kwargs)
        control.insert_fake_data(update_status)

    return {'current': 100, 'total': 100, 'status': 'Task completed!'}
