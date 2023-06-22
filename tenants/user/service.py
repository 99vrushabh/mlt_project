import uuid
from flask import request
from flask_login import current_user

from common.models import Signup

#function for user details 
def details_user():
    user_all = current_user
    return user_all

def signup_user():
    add_user=Signup(
    id =str(uuid.uuid4()),
    name=request.form.get("name"),  
    email=request.form.get("email"),
    phone = request.form.get("phone"),
    password=request.form.get("password"))
    return add_user 


def authenticate(email, password):
    user = Signup.query.filter_by(email=email).first()
    if user and user.password == password:
        return user
    return None