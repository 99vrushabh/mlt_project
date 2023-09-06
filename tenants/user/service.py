from datetime import date
import uuid
from flask import request
from flask_login import current_user
import jwt
from sqlalchemy import desc, func
from common.database import db
from common.models import Comments, New_store, Signup



#function for user details 
def details_user():
    user = current_user
    return user


# function for Signup user
def signup_user():
    id =str(uuid.uuid4())
    name=request.form.get("name")  
    email=request.form.get("email")
    phone = request.form.get("phone")
    password=request.form.get("password")
    payload = {'password': password}
    token = jwt.encode(payload, 'vrushabh@2611', algorithm='HS256')     
    new_passwrod = token 
    add_user = Signup(id=id,name=name,email=email,phone=phone,password = new_passwrod)
    db.session.add(add_user)
    db.session.commit()
    return add_user 



def authenticate():
    email = request.form.get('email')
    password = request.form.get('password')
    user = Signup.query.filter_by(email=email).first()
    if user:
        try:
            token = user.password
            new_password = jwt.decode(token, 'vrushabh@2611', algorithms='HS256')
            if user and new_password['password'] == password:
                return user
        except jwt.DecodeError: 
             pass
    return None


# give user access of  admin
def admin_user(user):
     if not user.is_admin:
                user.is_admin = True
                db.session.commit()


# function for add comment in a database
def comments(session,tenant):
    Comments.__table__.schema = tenant
    id = str(uuid.uuid4())
    comment_title = request.form.get("comment_title")
    comment_desc = request.form.get("comment_desc")
    comment_by = current_user.email
    comment_at = date.today()
    comment = Comments(id=id, comment_title=comment_title, comment_desc=comment_desc, comment_by=comment_by, comment_at=comment_at)
    session.add(comment)
    session.commit()
    session.close()
    return comment

# function for display new added stores

# function for display trending stores
def trend_stores(session):
    subquery = (
        session.query(New_store.id, func.max(New_store.visitors).label("max_visitors"))
        .filter(New_store.is_arch == False, current_user.is_admin == False)
        .group_by(New_store.id)
        .subquery()
    )
    
    new = (
        session.query(New_store)
        .join(subquery, New_store.id == subquery.c.id)
        .order_by(desc(subquery.c.max_visitors))
        .limit(6)
        
    )
    return new