from model import User, Account, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

################# DEALING WITH THE USER #################
class UserManagement:
    '''It receives data and manipulates to make CRUD operations with the user'''
    def create_user(self, name, email, password) -> None:
        '''It creates the user if the email is not being used'''
        password = self.__make_hash(password)
        user = User(name=name,
                    email=email,
                    password=password)
        exists = DbManagement().search_email(email)
        if exists: return False
        created_user = DbManagement().insert_user(user)
        return created_user

    def delete_user(self, id) -> str:
        '''It deletes the current user'''
        user = DbManagement().get_user(id)
        DbManagement().delete_user(user)

    def change_password(self, old_password, new_password, user) -> None:
        '''It checks the input passwords, if they match, it changes the user's one'''
        old_password = self.__make_hash(old_password)
        new_password = self.__make_hash(new_password)
        if old_password == new_password():
            user.password = new_password
            session.commit()
            return True
        return False

    def login(self, email, password) -> None:
        '''It checks the user's email and password'''
        user = DbManagement().search_email(email)
        password = self.__make_hash(password)
        if user.password == password:
            return user
        return False

    def __make_hash(self, password) -> str:
        '''It makes a hash with the received password'''
        from hashlib import sha256
        password = sha256(password.encode()).hexdigest()
        return password


class AccountManagement:
    '''It manipulates the user's account'''
    def create_account(self, id) -> None:
        '''It creates an account if the user does not have one yet'''
        if self.__search_account(id): return False
        account = Account(transaction='Account Opening',
                          reason='-',
                          amount=0,
                          balance=0, 
                          owner_id=id)
        try: session.add(account)
        except: 
            session.rollback()
            return False
        else:
            session.commit()
            return True

    def get_balance(self, owner_id) -> str:
        '''It returns a JSON with the user's balance'''
        data = session.query(Account).filter(Account.owner_id == owner_id).all()
        data_gathered = []
        for object in data: # excluir essa funcao e retornar apenas o dado cru do db
            data_json = {'balance': object.balance, 'reason': object.reason,
                         'amount': object.amount, 'transaction': object.transaction}
            data_gathered.append(data_json.copy())
            data_json.clear()
        return data_gathered

    def withdraw_money(self, owner_id, reason, amount) -> bool:
        '''It withdraws money from the user's account if they have enough money'''
        data = self.get_balance(owner_id)
        print(data)
        current_balance = float(data[-1]['balance'])
        amount = round(float(amount), 2)
        if current_balance >= float(amount):
            current_balance -= float(amount)
            expense = Account(transaction='Withdraw',
                              balance=float(current_balance),
                              owner_id=owner_id,
                              reason=reason,
                              amount=amount)
            session.add(expense)
            session.commit()
            return True
        else:
            return False

    def deposit_money(self, owner_id, reason, amount) -> bool:
        '''It deposits the received amount of money in the user's account'''
        data = self.get_balance(owner_id)
        current_balance = float(data[-1]['balance'])
        amount = round(float(amount), 2)
        current_balance += amount
        try:
            expense = Account(transaction='Deposit',
                              balance=float(current_balance),
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
        '''It receives an user id and searches for their account. If they do 
        not have one, it returns bool False'''
        data = session.query(Account).filter(Account.owner_id == owner_id).first()
        if data: return True
        return False

class DbManagement:
    '''It will manage the database for the user and the account class'''
    def insert_user(self, user) -> None:
        '''It receives an user object and insert it in the database'''
        try:
            session.add(user)
        except:
            session.rollback()
            return False
        else:
            session.commit()
            return True

    def delete_user(self, user) -> None:
        '''It receives an user object and removes it completely from the database
        if the user has an account, it will remove all of their balances'''
        try: session.delete(user)
        except: session.rollback()
        else: session.commit()
    
    def search_email(self, email) -> str:
        '''It searches in the database for an email and returns it if True'''
        try:
            user = session.query(User).filter(User.email == email.lower()).first()
            if user == None: raise ValueError
        except: return False
        else: return user
    
    def get_user(self, id) -> int:
        '''It searches in the database for an user by their ID and returns it'''
        user = session.query(User).filter(User.id == id).first()
        return user