from datetime import date
from flask_login import UserMixin
from sqlalchemy import ARRAY, Boolean, Column, Float, ForeignKey, Integer, String
from common.database import db

class Signup(UserMixin,db.Model):
    __table_args__ = {'schema':'myschema'}
    id = Column(String(50), primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    phone = Column(String(50),nullable=False)
    password = Column(String(250), unique=True, nullable=False)
    is_admin = Column(Boolean,default=False)
    is_superadmin = Column(Boolean,default=False)

class new_store(db.Model):
    __tablename__ = 'new_store'
    __table_args__ = {'schema':'myschema'}

    id = Column(String(50), primary_key=True)
    sname = Column(String(250), nullable=False , unique=True)
    semail = Column(String(50), unique=True, nullable=False)
    sphone = Column(String(50),nullable=False)
    spassword = Column(String(250), unique=True, nullable=False)
    create_by = Column(String(50),ForeignKey(Signup.email))
    create_at = Column(String(20),default=date.today(),nullable=False)
    update_at = Column(String(20),default=date.today(),nullable=False)
    is_active = Column(Boolean,default=True)
    is_arch = Column(Boolean,default=False) 


class Product(db.Model):
    __tablename__ = 'product'
    id = Column(String(50), primary_key=True)
    name = Column(String(50),nullable=False)
    pinfo = Column(String(100))
    pdesc = Column(String(150))
    price = Column(Integer,nullable=False)

class Comments(db.Model):
    __tablename__ = 'comments'
    id = Column(String(50), primary_key=True)
    comment_title = Column(String(250), nullable=False)
    comment_desc = Column(String(250), nullable=False)
    comment_by = Column(String(50),ForeignKey(Signup.email))


class Trace(db.Model):
    __tablename__ = 'Trace'
    __table_args__ = {'schema': 'myschema'}
    id = Column(String(50), primary_key=True)
    update_on = Column(String(50), ForeignKey(new_store.sname))
    update_at = Column(String(20), default=date.today(), nullable=False)
    update_by = Column(String(50), ForeignKey(Signup.email))