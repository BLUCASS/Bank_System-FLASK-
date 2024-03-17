from sqlalchemy import create_engine, String, Integer, Float, Column, ForeignKey
from flask_login import UserMixin
from sqlalchemy.orm import declarative_base, relationship

engine = create_engine('sqlite:///data.db')
Base = declarative_base()


class User(UserMixin, Base):
    from random import randint
    """Creating the User's column"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(80), nullable=False)
    ppsn = Column(Integer, default=randint(111111, 999999))
    account = relationship("Account", back_populates="user", cascade="all, delete-orphan")
    # CRIAR UMA RELACAO COM A OUTRA CLASSE PELO NOME, BACK_POP = NOME DA CLASSE EM MINUSCULA
    # DECLARA A CASCADE NA RAIZ DO DELETAR E TODAS AS RELATIONS SERAO ORFAS


class Account(Base):
    """Creating the User's Account column"""
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    balance = Column(Float)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    reason = Column(String)
    amount = Column(Float)
    
    user = relationship("User", back_populates="account")
    # CRIAR UMA RELACAO COM A OUTRA CLASSE PELO NOME, BACK_POP = NOME DA CLASSE EM MINUSCULA
    # DECLARA O FOREIGN_KEY/ONDELETE CASCADE EM TODAS AS ORFAS


Base.metadata.create_all(bind=engine)