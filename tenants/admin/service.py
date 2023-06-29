from datetime import date
import uuid
from flask import request
from flask_login import current_user
from sqlalchemy import text
from common.database import db
from common.models import Comments, Product, Trace, new_store




# function for add new store 
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
    comment_table = Comments.__table__
    create_schema_statement = (text(f'CREATE SCHEMA IF NOT EXISTS "{schema}"'))
    session.execute(create_schema_statement)

    set_search_path_statement = (text(f'SET search_path TO "{schema}"'))
    session.execute(set_search_path_statement)

    create_table_statement = (text(f'''
        CREATE TABLE IF NOT EXISTS "{schema}"."{product_table.name}" (
            {', '.join(column.name + ' ' + column.type.compile(dialect=session.bind.dialect) for column in product_table.columns)}
        )
    '''))

    create_table_statement2 = (text(f'''
        CREATE TABLE IF NOT EXISTS "{schema}"."{comment_table.name}" (
            {', '.join(column.name + ' ' + column.type.compile(dialect=session.bind.dialect) for column in comment_table.columns)}
        )
    '''))
    session.execute(create_table_statement)
    session.execute(create_table_statement2)

# function for product add
def product_add():
    add_product=Product(
            id =str(uuid.uuid4()),
            name=request.form.get("name"),  
            pinfo = request.form.get("pinfo"),
            pdesc = request.form.get("pdesc"),
            price=request.form.get("price")
            )
    return add_product  

# for add store to archive
def add_arch_store(tenant):
    if current_user.is_admin==True:
            store =  new_store.query.filter_by(sname=tenant).first()
            store.is_arch  = True
            db.session.commit()
 

# for edit  exist store's details
def update_store(store, db):
    store.sname = request.form.get('tname')
    store.semail = request.form.get('temail')
    store.sphone = request.form.get('tphone')
    store.spassword = request.form.get('tpassword')
    store.update_at = date.today()

    db.session.commit()

def new_update(store_name,user_email):
    new_update_details = Trace(
                id=str(uuid.uuid4()),
                update_on=store_name,
                update_by=user_email,
            )
    db.session.add(new_update_details)
    db.session.commit()