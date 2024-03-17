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

    def login(self, email, password) -> None:
        user = DbManagement().search_email(email)
        enc_password = self.__make_hash(password)
        if user:
            if user.password == enc_password:
                return user
        return False

    def __make_hash(self, password) -> str:
        from hashlib import sha256
        password = sha256(password.encode()).hexdigest()
        return password


class AccountManagement:

    def create_account(self, id) -> None:
        if self.__search_account(id): return False
        account = Account(balance=0, owner_id=id, reason='Account Creation')
        try: session.add(account)
        except: 
            session.rollback()
            return False
        else:
            session.commit()
            return True

    def get_balance(self, owner_id) -> str:
        data = session.query(Account).filter(Account.owner_id == owner_id).all()
        return data

    def withdraw_money(self, owner_id, reason, amount) -> bool:
        data = self.get_balance(owner_id)
        current_balance = float(data[-1].balance)
        amount = round(float(amount), 2)
        print(amount)
        if current_balance >= float(amount):
            current_balance -= float(amount)
            expense = Account(balance=float(current_balance),
                              owner_id=owner_id,
                              reason=reason,
                              amount=amount)
            session.add(expense)
            session.commit()
            return True
        else:
            return False

    def deposit_money(self, owner_id, reason, amount) -> bool:
        data = self.get_balance(owner_id)
        current_balance = float(data[-1].balance)
        amount = round(float(amount), 2)
        current_balance += amount
        try:
            expense = Account(balance=float(current_balance),
                                owner_id=owner_id,
                                reason=reason,
                                amount=amount)
            session.add(expense)
        except:
            session.rollback()
            return False
        else:
            session.commit()
            return True

    def __search_account(self, owner_id) -> bool:
        data = session.query(Account).filter(Account.owner_id == owner_id).first()
        if data: return True
        return False

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
    
    def get_user(self, id) -> int:
        user = session.query(User).filter(User.id == id).first()
        return user