from model import User, Account, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()


class UserManagement:

    def create_user(self, data) -> None:
        password = self.__make_hash(data["password"])
        user = User(name=data["name"].title(),
                    email=data["email"].lower(),
                    password=password)
        exists = DbManagement().search_email(data["email"])
        if exists: return False
        DbManagement().insert_user(user)

    def delete_user(self, data) -> str:
        user = DbManagement().search_email(data["email"])
        if user: 
            if user.password == self.__make_hash(data["password"]):
                DbManagement().delete_user(user)

    def change_password(self, data) -> None:
        user = DbManagement().search_email(data["email"])
        if user: 
            if user.password == self.__make_hash(data["old_password"]):
                user.password = self.__make_hash(data["new_password"])
                session.commit()

    def __make_hash(self, password) -> str:
        from hashlib import sha256
        password = sha256(password.encode()).hexdigest()
        return password


class AccountManagement:

    pass


class DbManagement:

    def insert_user(self, user) -> None:
        try:
            session.add(user)
        except:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()

    def delete_user(self, user) -> None:
        try: session.delete(user)
        except: session.rollback()
        else: session.commit()
    
    def search_email(self, email) -> str:
        try:
            user = session.query(User).filter(User.email == email.lower()).first()
            if user == None: raise ValueError
        except: return False
        else: return user