import math
import copy
from sqlalchemy import text, desc
import plotly.express as px
import pandas as pd
from dataclasses import dataclass

from .model import IncomeAndExpense, Savings, Jar, Jars
from .. import db
from ..utils import CustomizeError


@dataclass
class DataColumn:
    income_and_expense: str = '收入或支出'
    money: str = '金額'
    jar_name: str = '帳戶'
    date: str = '日期'
    remark: str = '備註'


class IncomeAndExpenseControl:
    def __init__(self, **kwargs):
        self.__kwargs = kwargs
        self.__response_data = copy.deepcopy(kwargs)
        self.__saving = None
        self.__distribution_money_list = None
        self.__income_and_expense_id = None

    def query_chart(self):
        income_and_expense_object = self.__query_income_and_expense_object()
        df_records = self.__object_to_df(income_and_expense_object)
        df_records = self.__organize_data(df_records)
        chart_json = self.__create_chart(df_records)
        return chart_json

    def __object_to_df(self, income_and_expense_object):
        df_records = pd.DataFrame.from_records(income_and_expense_object.all(),
                                               columns=['object',
                                                        'id',
                                                        'income_and_expense',
                                                        'money',
                                                        'date',
                                                        'remark',
                                                        'jar_name'])
        return df_records

    def __create_chart(self, df_records):
        if self.__kwargs['chart_type'] == "直方":
            fig = px.histogram(df_records,
                               x=DataColumn.money,
                               color=DataColumn.income_and_expense)
        elif self.__kwargs['chart_type'] == "長條":
            fig = px.bar(df_records,
                         x=DataColumn.jar_name,
                         y=DataColumn.money,
                         color=DataColumn.income_and_expense)
        elif self.__kwargs['chart_type'] == "圓餅":
            fig = px.pie(df_records,
                         values=DataColumn.money,
                         names=DataColumn.jar_name)
        elif self.__kwargs['chart_type'] == "折線":
            fig = px.line(df_records,
                          x=DataColumn.date,
                          y=DataColumn.money,
                          color=DataColumn.jar_name)
        elif self.__kwargs['chart_type'] == "散佈":
            fig = px.scatter(df_records,
                             x=DataColumn.jar_name,
                             y=DataColumn.money,
                             size=DataColumn.money,
                             color=DataColumn.income_and_expense)
        return fig.to_json()

    def __organize_data(self, df_records):
        df_records = df_records.drop(["object", 'id','remark'], axis=1)
        df_records['income_and_expense'] = df_records['income_and_expense'].apply(
            lambda x: '收入' if x == "income" else "支出")
        df_records.rename(columns={'income_and_expense': DataColumn.income_and_expense,
                                   'money': DataColumn.money,
                                   'date': DataColumn.date,
                                   'remark': DataColumn.remark,
                                   'jar_name': DataColumn.jar_name
                                   }, inplace=True)
        return df_records

    def query_list(self) -> object:
        income_and_expense_object = self.__query_income_and_expense_object()
        page_objs = self.__make_pagination(income_and_expense_object)
        return [row._mapping for row in page_objs.items], page_objs.total

    def __query_income_and_expense_object(self):
        order_by = self.__create_order_by()
        filter = self.__create_filter()
        return self.__query(filter, order_by)

    def __create_order_by(self):
        if self.__kwargs.get("sort") == "money":
            order_by = IncomeAndExpense.money
        elif self.__kwargs.get("sort") == "date":
            order_by = IncomeAndExpense.date
        elif self.__kwargs.get("sort") == "jar_name":
            order_by = Jar.name
        else:
            order_by = IncomeAndExpense.date
        if self.__kwargs['sortOrder'] == "desc":
            order_by = desc(order_by)
        return order_by

    def __create_filter(self):
        filter = f"income_and_expense.user_id={self.__kwargs['user_id']} "
        filter = self.__add_income_and_expense_to_filter(filter)
        filter = self.__add_jar_name_to_filter(filter)
        filter = self.__add_money_to_filter(filter)
        filter = self.__add_date_to_filter(filter)
        return filter

    def __query(self, filter, order_by):
        income_and_expense_object_list = IncomeAndExpense.query \
            .join(Jar, IncomeAndExpense.jar_id == Jar.id) \
            .add_columns(IncomeAndExpense.id,
                         IncomeAndExpense.income_and_expense,
                         IncomeAndExpense.money,
                         IncomeAndExpense.date,
                         IncomeAndExpense.remark,
                         Jar.name.label('jar_name')) \
            .filter(text(filter)) \
            .order_by(order_by)
        return income_and_expense_object_list

    def __make_pagination(self, income_and_expense_object):
        page_objs = income_and_expense_object.paginate(page=self.__kwargs["page"], per_page=self.__kwargs["limit"])
        return page_objs

    def __add_income_and_expense_to_filter(self, filter):
        if self.__kwargs.get('income_and_expense'):
            filter += f" and income_and_expense.income_and_expense = '{self.__kwargs['income_and_expense']}' "
        return filter

    def __add_jar_name_to_filter(self, filter):
        if self.__kwargs.get('jar_name'):
            filter += f" and jar.name = '{self.__kwargs['jar_name']}' "
        return filter

    def __add_money_to_filter(self, filter):
        filter = self.__add_maximum_money_to_filter(filter)
        filter = self.__add_minimum_money_to_filter(filter)
        return filter

    def __add_date_to_filter(self, filter):
        filter = self.__add_earliest_date_to_filter(filter)
        filter = self.__add_latest_date_to_filter(filter)
        return filter

    def __add_maximum_money_to_filter(self, filter):
        if self.__kwargs.get('maximum_money'):
            filter += f" and income_and_expense.money <= '{self.__kwargs['maximum_money']}' "
        return filter

    def __add_minimum_money_to_filter(self, filter):
        if self.__kwargs.get('minimum_money'):
            filter += f" and income_and_expense.money >= '{self.__kwargs['minimum_money']}' "
        return filter

    def __add_latest_date_to_filter(self, filter):
        if self.__kwargs.get('latest_date'):
            filter += f" and income_and_expense.date <= '{self.__kwargs['latest_date']}' "
        return filter

    def __add_earliest_date_to_filter(self, filter):
        if self.__kwargs.get('earliest_date'):
            filter += f" and income_and_expense.date >= '{self.__kwargs['earliest_date']}' "
        return filter

    def read(self):
        income_and_expense = IncomeAndExpense.query.filter_by(id=self.__kwargs["id"]).first()
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
            db.session.add_all([savings, income_and_expense])
        self.__saving = savings.savings
        self.__response_data["id"] = income_and_expense.id

    def __add_record(self):
        self.__jar_id = self.__return_jar_id()
        income_and_expense = self.__add_record_to_income_and_expense_table()
        savings = self.__add_record_to_saving_table()
        return savings, income_and_expense

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

    def __caluate_distribution_money(self):
        money = self.__kwargs["all_money"]
        distribution_money_list = [math.floor(money * ratio) for ratio in Jars.ratio()]
        over = money - sum(distribution_money_list)
        distribution_money_list[0] += over
        return distribution_money_list

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
        income_and_expense = IncomeAndExpense.query.filter_by(id=self.__kwargs["id"]).first()
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

    def __give_sign(self, income_and_expense, reverse=False):
        if reverse:
            return -1 if income_and_expense == "income" else 1
        else:
            return 1 if income_and_expense == "income" else -1

    def __return_jar_id(self):
        return Jars.names().index(self.__kwargs["jar_name"]) + 1

    def init_savings(self):
        if Savings.query.filter_by(user_id=self.__kwargs["user_id"]).first() is None:
            savings_list = [Savings(savings=0, jar_id=i, user_id=self.__kwargs["user_id"])
                            for i in range(1, Jars.length() + 1)]
            db.session.add_all(savings_list)
            db.session.commit()
        else:
            print("init_savings not none")

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
