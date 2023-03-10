import unittest
from flask import url_for
from flask_testing import TestCase
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash
import re
from datetime import datetime

from app import create_app, db
from app.utils import CustomizeError
from app.db_init_data import jar_dict
from app.user.model import User
from app.six_jar.control import IncomeAndExpenseControl
from app.six_jar.model import IncomeAndExpense, Savings, Jar


class SettingBase(TestCase):

    def create_app(self):
        print("start test")
        return create_app()

    def setUp(self):
        # setUp每個獨立測試前置 setUpClass一整個class的前置(會造成test互相干擾)
        self.__check_env()
        db.drop_all()
        db.create_all()
        self.__init_value()
        self.__insert_test_user()
        self.__insert_savings()
        self.__insert_test_income_and_expense()

    def tearDown(self):
        db.drop_all()
        db.session.remove()

    def __check_env(self):
        load_dotenv()
        if os.environ["PYTHON_WEB_CONFIG"] != "local_test":
            raise CustomizeError('測試環境設定錯誤，not local_test')

    def __init_value(self):
        self.user_id = 1
        self.user_name = "test"
        self.user_email = "test@gmail.com"
        self.user_password = "test"
        self.income_and_expense_id = 1
        self.money = 12345
        self.date = datetime.strptime("2022-02-02", '%Y-%m-%d').date()
        self.jar_name = "休閒玩樂"
        self.jar_id = list(jar_dict.keys()).index(self.jar_name) + 1
        self.income_and_expense = "expense"
        self.remark = "測試備註"

    def __insert_test_user(self):
        user = User(email=self.user_email, name=self.user_name, password=generate_password_hash(self.user_password))
        db.session.add(user)
        db.session.commit()

    def __insert_test_income_and_expense(self):
        control = IncomeAndExpenseControl(
            income_and_expense=self.income_and_expense,
            money=self.money,
            date=self.date,
            remark=self.remark,
            user_id=self.user_id,
            jar_name=self.jar_name)
        control.insert()
        saving = Savings.query.filter_by(user_id=self.user_id, jar_id=self.jar_id).first()
        if self.income_and_expense == "expense":
            sign = -1
        else:
            sign = 1
        self.assertEqual(saving.savings, sign * self.money)

    def __insert_savings(self):
        control = IncomeAndExpenseControl(user_id=self.user_id)
        control.init_savings()
        saving_list = Savings.query.filter_by(user_id=self.user_id).all()
        for saving in saving_list:
            self.assertEqual(saving.savings, 0)

    def login(self):
        response = self.client.post(url_for('api.userloginapi'),
                                    json={
                                        "email": self.user_email,
                                        "password": self.user_password,
                                        "remember_me": True
                                    })
        return response

    def get_csrf_access_token(self):
        response = self.login()
        for cookie in response.headers.get_all('Set-Cookie'):
            csrf_access_token = re.match("csrf_access_token=(.*);", cookie)
            if csrf_access_token:
                return csrf_access_token.group(1)
        else:
            return None
