import math
import copy

from .model import IncomeAndExpense, Savings, Jar, Jars
from .. import db


class IncomeAndExpenseControl:
    def __init__(self, **kwargs):
        self.__kwargs = kwargs
        self.__response_data = copy.deepcopy(kwargs)
        self.__user_id = self.__kwargs["user_id"]
        self.__saving = None
        self.__distribution_money_list = None
        self.__income_and_expense_id = None

    def read(self, id):
        income_and_expense = IncomeAndExpense.query.filter_by(id=id).first()
        if income_and_expense:
            self.__response_data = {
                "user_id": self.__user_id,
                "income_and_expense": income_and_expense.income_and_expense,
                "money": income_and_expense.money,
                "date": income_and_expense.date,
                "remark": income_and_expense.remark,
                "jar_name": Jars.names()[income_and_expense.jar_id]
            }
            return True
        else:
            return False

    def insert(self):
        income_and_expense = self.__add_reord_to_income_and_expense_table()
        savings = self.__add_reord_to_saving_table()
        db.session.add(income_and_expense)
        db.session.add(savings)
        db.session.commit()
        self.__saving = savings.savings
        self.__response_data["income_and_expense_id"] = income_and_expense.id

    def auto_insert_income(self):
        distribution_money_list = self.__caluate_distribution_money(self.__kwargs["all_money"])
        for index, distribution_money in enumerate(distribution_money_list):
            self.__kwargs["income_and_expense"] = "income"
            self.__kwargs["money"] = distribution_money
            self.__kwargs["jar_name"] = Jars.names()[index]
            self.insert()
        self.__distribution_money_list = distribution_money_list

    def update(self):
        self.__update_reord_to_income_and_expense_table()
        self.__update_reord_to_saving_table()

    def delete(self):
        self.__delete_reord_to_income_and_expense_table()
        self.__update_reord_to_saving_table()

    def __caluate_distribution_money(self, money):
        distribution_money_list = [math.floor(money * ratio) for ratio in Jars.ratio()]
        over = money - sum(distribution_money_list)
        distribution_money_list[0] += over
        return distribution_money_list

    def __update_reord_to_income_and_expense_table(self):
        update_dict = {"name": name,
                       "password": generate_password_hash(password)}
        row_cowunt = db.session.query(IncomeAndExpense).filter_by(id=id).update(update_dict)
        if row_cowunt != 1:
            return False
        else:
            db.session.commit()
            return True

    def __update_reord_to_saving_table(self):
        pass
        # 計算新舊金額差距，更動到存款

    def __add_reord_to_income_and_expense_table(self):
        print(self.__kwargs)
        income_and_expense = IncomeAndExpense(
            income_and_expense=self.__kwargs["income_and_expense"],
            money=self.__kwargs["money"],
            date=self.__kwargs["date"],
            remark=self.__kwargs.get("remark"),
            user_id=self.__user_id,
            jar_id=Jar.query.filter_by(name=self.__kwargs["jar_name"]).first().id
        )
        return income_and_expense

    def __add_reord_to_saving_table(self):
        jar_name = self.__kwargs["jar_name"]
        income_and_expense = self.__kwargs["income_and_expense"]
        money = self.__kwargs["money"]

        savings = Savings.query \
            .filter(Savings.user_id == self.__user_id) \
            .filter(Savings.jar_id == (Jars.names().index(jar_name) + 1)) \
            .first()
        sign = 1 if income_and_expense == "income" else -1
        savings.savings += money * sign
        return savings

    def init_savings(self):
        if Savings.query.filter_by(user_id=self.__user_id).first() is None:
            savings_list = [Savings(savings=0, jar_id=i, user_id=user_id) for i in range(1, Jars.length() + 1)]
            db.session.add_all(savings_list)
            db.session.commit()

    def get_saving_list(self):
        saving_object_list = Savings.query \
            .join(Jar, Savings.jar_id == Jar.id) \
            .add_columns(Savings.savings, Jar.name) \
            .filter(Savings.user_id == self.__user_id) \
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
