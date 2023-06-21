import uuid
from flask import render_template, request
from flask_login import current_user
from sqlalchemy import text

from common.models import Product, Signup, new_store


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


def store_add():
    new_add=new_store(id = str(uuid.uuid4()),
    sname = request.form.get('sname').lower().replace(" ", "_"),
    semail = request.form.get('semail'),
    sphone = request.form.get("sphone"),
    spassword = request.form.get('spassword'),
    create_by = str(current_user.email))
    return new_add



def create_table_store(session, schema):
    product_table = Product.__table__
    create_schema_statement = (text(f'CREATE SCHEMA IF NOT EXISTS "{schema}"'))
    session.execute(create_schema_statement)

    set_search_path_statement = (text(f'SET search_path TO "{schema}"'))
    session.execute(set_search_path_statement)

    create_table_statement = (text(f'''
        CREATE TABLE IF NOT EXISTS "{schema}"."{product_table.name}" (
            {', '.join(column.name + ' ' + column.type.compile(dialect=session.bind.dialect) for column in product_table.columns)}
        )
    '''))

    session.execute(create_table_statement)



def product_add():
    add_product=Product(
            id =str(uuid.uuid4()),
            name=request.form.get("name"),  
            pinfo = request.form.get("pinfo"),
            pdesc = request.form.get("pdesc"),
            price=request.form.get("price")
            )
    return add_product 

def find_store(search):
    msg="fetch error"
    if search:
        search_stores = new_store.query.filter(new_store.sname.like(f'%{search}%')).all()
        if not search_stores:
            msg = "Store not found"
        return search_stores,msg
    else:
        return [],msg
    
def search_products(session, search, schema):
    msg=""
    if search:
        searchproducts = session.execute(
            text(f'SELECT * FROM "{schema}"."product" WHERE LOWER(name) LIKE :value'),
            {"value": f"%{search}%"}
        )
        if not searchproducts:
            msg = "Product not found"
            return msg
        else:
            # process the search products result
            return searchproducts.fetchall()
    else:
        return [],msg
    
def all_products(session, schema):
    display = text(f'SELECT * FROM "{schema}"."product" ')
    menu = session.execute(display)
    return menu.fetchall()
