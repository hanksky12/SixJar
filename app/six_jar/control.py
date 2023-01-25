import math
import copy

from .model import IncomeAndExpense, Savings, Jar, Jars
from .. import db
from ..utils import CustomizeError


class IncomeAndExpenseControl:
    def __init__(self, **kwargs):
        self.__kwargs = kwargs
        self.__response_data = copy.deepcopy(kwargs)
        self.__saving = None
        self.__distribution_money_list = None
        self.__income_and_expense_id = None

    def read(self):
        income_and_expense = IncomeAndExpense.query.filter_by(id=self.__kwargs["income_and_expense_id"]).first()
        if income_and_expense:
            self.__response_data = {
                "user_id": self.__kwargs["user_id"],
                "income_and_expense": income_and_expense.income_and_expense,
                "money": income_and_expense.money,
                "date": income_and_expense.date,
                "remark": income_and_expense.remark,
                "jar_name": Jars.names()[income_and_expense.jar_id]
            }
        else:
            raise CustomizeError.no_record_find()

    def insert(self):
        with db.auto_commit():
            savings, income_and_expense = self.__add_record()
            db.session.add([savings, income_and_expense])
        self.__saving = savings.savings
        self.__response_data["income_and_expense_id"] = income_and_expense.id

    def auto_insert_income(self):
        distribution_money_list = self.__caluate_distribution_money()
        with db.auto_commit():
            for index, distribution_money in enumerate(distribution_money_list):
                self.__kwargs["income_and_expense"] = "income"
                self.__kwargs["money"] = distribution_money
                self.__kwargs["jar_name"] = Jars.names()[index]
                savings, income_and_expense = self.__add_record()
                db.session.add_all([savings, income_and_expense])
        self.__distribution_money_list = distribution_money_list

    def update(self):
        with db.auto_commit():
            income_and_expense = self.__query_income_and_expense()
            self.__update_savings(income_and_expense, is_reverse=True)
            income_and_expense = self.__update_record_to_income_and_expense_table(income_and_expense)
            self.__update_savings(income_and_expense, is_reverse=False)

    def delete(self):
        with db.auto_commit():
            income_and_expense = self.__query_income_and_expense()
            self.__update_savings(income_and_expense, is_reverse=True)
            db.session.delete(income_and_expense)

    def __query_income_and_expense(self):
        income_and_expense = IncomeAndExpense.query.filter_by(id=self.__kwargs["income_and_expense_id"]).first()
        if income_and_expense is None:
            raise CustomizeError.no_record_find_or_number_unusual()
        return income_and_expense

    def __update_savings(self, income_and_expense, is_reverse):
        savings = Savings.query \
            .filter(Savings.user_id == self.__kwargs["user_id"]) \
            .filter(Savings.jar_id == income_and_expense.jar_id) \
            .first()
        savings.savings += \
            income_and_expense.money * self.__give_sign(income_and_expense.income_and_expense, reverse=is_reverse)

    def __update_record_to_income_and_expense_table(self, income_and_expense):
        income_and_expense.money = self.__kwargs["money"]
        income_and_expense.income_and_expense = self.__kwargs["income_and_expense"]
        income_and_expense.date = self.__kwargs["date"]
        income_and_expense.remark = self.__kwargs.get("remark")
        income_and_expense.jar_id = self.__return_jar_id()
        return income_and_expense

    def __add_record(self):
        self.__jar_id = self.__return_jar_id()
        income_and_expense = self.__add_record_to_income_and_expense_table()
        savings = self.__add_record_to_saving_table()
        return savings, income_and_expense

    def __caluate_distribution_money(self):
        money = self.__kwargs["all_money"]
        distribution_money_list = [math.floor(money * ratio) for ratio in Jars.ratio()]
        over = money - sum(distribution_money_list)
        distribution_money_list[0] += over
        return distribution_money_list

    def __add_record_to_income_and_expense_table(self):
        income_and_expense = IncomeAndExpense(
            income_and_expense=self.__kwargs["income_and_expense"],
            money=self.__kwargs["money"],
            date=self.__kwargs["date"],
            remark=self.__kwargs.get("remark"),
            user_id=self.__kwargs["user_id"],
            jar_id=self.__jar_id
        )
        return income_and_expense

    def __add_record_to_saving_table(self):
        savings = Savings.query \
            .filter(Savings.user_id == self.__kwargs["user_id"]) \
            .filter(Savings.jar_id == self.__jar_id) \
            .first()
        savings.savings += \
            self.__kwargs["money"] * self.__give_sign(self.__kwargs["income_and_expense"])
        return savings

    def __return_jar_id(self):
        return Jars.names().index(self.__kwargs["jar_name"]) + 1


    def __give_sign(self, income_and_expense, reverse=False):
        if reverse:
            return -1 if income_and_expense == "income" else 1
        else:
            return 1 if income_and_expense == "income" else -1

    def init_savings(self):
        if Savings.query.filter_by(user_id=self.__kwargs["user_id"]).first() is None:
            savings_list = [Savings(savings=0, jar_id=i, user_id=self.__kwargs["user_id"])
                            for i in range(1, Jars.length() + 1)]
            db.session.add_all(savings_list)
            db.session.commit()

    def get_saving_list(self):
        saving_object_list = Savings.query \
            .join(Jar, Savings.jar_id == Jar.id) \
            .add_columns(Savings.savings, Jar.name) \
            .filter(Savings.user_id == self.__kwargs["user_id"]) \
            .order_by(Savings.jar_id).all()
        return saving_object_list

    @property
    def saving(self):
        return self.__saving

    @property
    def distribution_money_list(self):
        return self.__distribution_money_list

    @property
    def response_data(self):
        return self.__response_data


class IncomeAndExpenseConcentration:

    def __init__(self, income_and_expense):
        self.jar_id = income_and_expense.jar_id
        self.money = income_and_expense.money
        self.income_and_expense = income_and_expense.income_and_expense

    def __str__(self):
        return f"{self.jar_id} {self.money} {self.income_and_expense}"