from datetime import date
from flask_login import UserMixin
from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from common.database import db

class Signup(UserMixin,db.Model):
    __table_args__ = {'schema':'myschema'}
    id = Column(String(50), primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(250), unique=True, nullable=False)
    is_admin = Column(Boolean,default=False)
    is_superadmin = Column(Boolean,default=False)

class new_store(db.Model):
    __tablename__ = 'new_store'
    __table_args__ = {'schema':'myschema'}

    id = Column(String(50), primary_key=True)
    sname = Column(String(250), nullable=False)
    semail = Column(String(50), unique=True, nullable=False)
    spassword = Column(String(250), unique=True, nullable=False)
    create_by = Column(String(50),ForeignKey(Signup.email))
    create_at = Column(String(20),default=date.today(),nullable=False)



