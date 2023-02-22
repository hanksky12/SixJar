import unittest
from flask import url_for
from flask_testing import TestCase
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash
import re

from app import create_app, db
from app.six_jar.model import Jar
from app.user.model import User
from app.utils import CustomizeError


class SettingBase(TestCase):
    def create_app(self):
        return create_app()

    def setUp(self):
        self.__check_env()
        self.__init_test_value()
        self.__insert_test_user()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def __check_env(self):
        load_dotenv()
        if os.environ["PYTHON_WEB_CONFIG"] != "local_test":
            raise CustomizeError('測試環境設定錯誤，not local_test')

    def __init_test_value(self):
        self.user_name = "test"
        self.user_email = "test@gmail.com"
        self.user_password = "test"
        self.money = 12345
        self.date = "2022-02-02"
        self.jar_name = "休閒玩樂"
        self.user_id = "1"
        self.income_and_expense = "expense"

    def __insert_test_user(self):
        user = User(email=self.user_email, name=self.user_name, password=generate_password_hash(self.user_password))
        db.session.add(user)
        db.session.commit()

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


