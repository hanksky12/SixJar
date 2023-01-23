

from .model import IncomeAndExpense, Savings, Jar, Jars
from .. import db

class IncomeAndExpenseControl:
    def __init__(self, user_id):
        self.__user_id = user_id
        self.__saving = None

    def add(self, **kwargs):
        self.__add_reord_to_income_and_expense_table(**kwargs)
        self.__add_reord_to_saving_table(**kwargs)
        db.session.commit()


    def __add_reord_to_income_and_expense_table(self, **kwargs):
        print(kwargs)
        income_and_expense= IncomeAndExpense(
            income_and_expense=kwargs["income_and_expense"],
            money=kwargs["money"],
            date=kwargs["date"],
            remark=kwargs["remark"],
            user_id=self.__user_id,
            jar_id=Jar.query.filter_by(name=kwargs["jar_name"]).first().id
        )
        db.session.add(income_and_expense)

    def __add_reord_to_saving_table(self, **kwargs):
        jar_name = kwargs["jar_name"]
        income_and_expense = kwargs["income_and_expense"]
        money = kwargs["money"]
        savings = Savings.query.filter(Savings.user_id == self.__user_id) \
            .filter(Savings.jar_id == Jars.names_dict()[jar_name]).first()
        sign = 1 if income_and_expense == "income" else -1
        savings.savings += money * sign
        db.session.add(savings)
        self.__saving = savings.savings


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









