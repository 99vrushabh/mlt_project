import uuid
from flask import render_template, request
from flask_login import current_user

from common.models import Signup, new_store


def details_user():
    user_name = current_user.name
    return {user_name}

def signup_user():
    add_user=Signup(
    id =str(uuid.uuid4()),
    name=request.form.get("name"),  
    email=request.form.get("email"),
    phone = request.form.get("phone"),
    password=request.form.get("password"))
    return add_user 

def find_store(search):
    msg="fetch error"
    if search:
        search_stores = new_store.query.filter(new_store.sname.like(f'%{search}%')).all()
        if not search_stores:
            msg = "Store not found"
        return search_stores,msg
    else:
        return [],msg