from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import logout_user, login_user
import time

from .model import User
from .. import db
from ..utils import JwtTool, CustomizeError


class UserControl:
    def __init__(self):
        self.__id = None
        self.__user = None

    def login(self, email, password, remember_me, returnResp):
        user = User.query.filter_by(email=email).first()
        if user is None or user.check_password(password) is False:
            raise CustomizeError("帳號不存在或密碼錯誤")
        self.__id = user.id
        self.__user = user
        resp = returnResp(user.id)
        self.__set_cookie(resp)
        login_user(user, remember_me)
        return resp

    def __set_cookie(self, resp):
        JwtTool.setting_cookie(resp, self.__id)
        resp.set_cookie(key='user_id', value=str(self.__id), expires=time.time() + 60 * 60* 60)

    def logout(self, resp):
        JwtTool.unset_cookie(resp)
        logout_user()
        resp.set_cookie(key='user_id', expires=0)

    def register(self, email, name, password):
        user = User(
            email=email,
            name=name,
            password=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        self.__id = user.id

    def delete_info(self, id):
        row_cowunt = db.session.query(User).filter_by(id=id).delete()
        if row_cowunt != 1:
            return False
        else:
            db.session.commit()
            return True

    def change_info(self, id, name, password):
        update_dict = {"name": name,
                       "password": generate_password_hash(password)}
        row_cowunt = db.session.query(User).filter_by(id=id).update(update_dict)
        if row_cowunt != 1:
            return False
        else:
            db.session.commit()
            return True

    @property
    def user_id(self):
        return self.__id

    @property
    def user(self):
        return self.__user
