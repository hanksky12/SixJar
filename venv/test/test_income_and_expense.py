from flask import url_for

from datetime import datetime

from app.six_jar.control import IncomeAndExpenseControl
from app.six_jar.model import IncomeAndExpense, Savings
from setting_base import SettingBase
from app.db_init_data import jar_dict


class IncomeAndExpenseTest(SettingBase):
    def test_automatic_allocation_money(self):
        waiting_for_allocation_money = 1000
        old_total_saving = self.__query_total_saving()
        self.__allocation_money(waiting_for_allocation_money)
        new_total_saving = self.__query_total_saving()
        self.assertEqual(old_total_saving + waiting_for_allocation_money, new_total_saving)

    def __allocation_money(self, waiting_for_allocation_money):
        control = IncomeAndExpenseControl(
            user_id=self.user_id,
            all_money=waiting_for_allocation_money,
            date=self.date,
            remark="",
        )
        control.auto_insert_income()

    def __query_total_saving(self):
        control = IncomeAndExpenseControl(user_id=self.user_id)
        savings_list = control.get_saving_list()
        total_saving = sum([saving[1] for saving in savings_list])
        return total_saving

    def test_update(self):
        update_money = 1000
        update_date = datetime.strptime("2222-02-07", '%Y-%m-%d').date()
        update_jar_name = "長期儲蓄"
        update_jar_id = list(jar_dict.keys()).index(update_jar_name) + 1
        update_income_and_expense = "expense"
        self.__update(update_money, update_date, update_jar_name, update_income_and_expense)
        self.__check_saving(update_jar_id, update_money)
        self.__check_record(update_money, update_date, update_jar_id, update_income_and_expense)

    def __update(self, update_money, update_date, update_jar_name, update_income_and_expense):
        control = IncomeAndExpenseControl(id=self.income_and_expense_id,
                                          user_id=self.user_id,
                                          money=update_money,
                                          date=update_date,
                                          jar_name=update_jar_name,
                                          income_and_expense=update_income_and_expense)

        control.update()

    def __check_saving(self, update_jar_id, update_money):
        saving_list = Savings.query.filter_by(user_id=self.user_id).all()
        new_jar_after_change_money = saving_list[update_jar_id - 1].savings
        old_jar_after_restored_money = saving_list[self.jar_id - 1].savings
        self.assertEqual(new_jar_after_change_money, -update_money)
        self.assertEqual(old_jar_after_restored_money, 0)

    def __check_record(self, update_money, update_date, update_jar_id, update_income_and_expense):
        income_and_expense = IncomeAndExpense.query.filter_by(id=self.income_and_expense_id).first()
        self.assertEqual(income_and_expense.money, update_money)
        self.assertEqual(income_and_expense.date, update_date)
        self.assertEqual(income_and_expense.jar_id, update_jar_id)
        self.assertEqual(income_and_expense.income_and_expense, update_income_and_expense)
