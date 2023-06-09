from flask_login import UserMixin
from sqlalchemy import Boolean, Column, Float, Integer, String
from common.database import db

class Signup(UserMixin,db.Model):
    __table_args__ = {'schema':'myschema'}
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(250), unique=True, nullable=False)
    is_admin = Column(Boolean,default=False)
    is_superadmin = Column(Boolean,default=False)

class new_store(db.Model):
    __tablename__ = 'store'
    __table_args__ = {'schema':'myschema'}

    id = Column(Integer, primary_key=True)
    sname = Column(String(250), nullable=False)
    semail = Column(String(50), unique=True, nullable=False)
    spassword = Column(String(250), unique=True, nullable=False)



class Product(db.Model):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    field1 =Column(String(100),nullable=False)
    field2 =Column(String(100),nullable=True)
    field3 =Column(String(100),nullable=True)
    price = Column(Float, nullable=False)

    