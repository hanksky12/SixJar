from flask import url_for
from setting_base import SettingBase


# class IncomeAndExpenseTest(SettingBase):
#     def test_post(self):
#         csrf_access_token = self.get_csrf_access_token()
#         response = self.client.post(url_for('api.api.incomeandexpensepostapi'),
#                                    headers={"X-CSRF-TOKEN": csrf_access_token},
#                                    json={
#                                        "money": self.money,
#                                        "date": self.date,
#                                        "jar_name": self.jar_name,
#                                        "user_id": self.user_id,
#                                        "income_and_expense": self.income_and_expense
#                                    }
#                                    )
#         self.assertEqual(response.status_code, 200)
