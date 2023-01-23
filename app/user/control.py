from werkzeug.security import generate_password_hash, check_password_hash


from .model import User
from .. import db

class UserControl:
    def __init__(self):
        self.__id = None
        self.__user = None


    def login(self, email, password):
        user = User.query.filter_by(email=email).first()
        if user is None:
            return False
        if user.check_password(password) is False:
            return False
        self.__id = user.id
        self.__user = user
        return True

    # def logout(self):

    def register(self, email, name, password):
        user = User(
            email=email,
            name=name,
            password=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()



    def change_info(self, id ,name, password):
        update_dict = {"name":name,
                       "password":generate_password_hash(password)}
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