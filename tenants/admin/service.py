from datetime import date
import uuid
from flask import request
from flask_login import current_user
from sqlalchemy import text
from common.database import db
from common.models import Comments, New_store, Product, Suggestion, Trace, Visit
from flask import redirect, request, url_for
from flask_login import current_user
from sqlalchemy import text



# function for add new store
def store_add():
    new_add = New_store(id=str(uuid.uuid4()),
                        sname=request.form.get(
                            'sname').lower().replace(" ", "_"),
                        semail=request.form.get('semail'),
                        sphone=request.form.get("sphone"),
                        spassword=request.form.get('spassword'),
                        create_by=str(current_user.email))
    return new_add

# function for that store which create their own schema 
def create_table_store(session, schema):
    product_table = Product.__table__
    comment_table = Comments.__table__
    visit_table = Visit.__table__
    create_schema_statement = (text(f'CREATE SCHEMA IF NOT EXISTS "{schema}"'))
    session.execute(create_schema_statement)
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
    create_table_statement3 = (text(f'''
       CREATE TABLE IF NOT EXISTS "{schema}"."{visit_table.name}" (
            {', '.join(column.name + ' ' + column.type.compile(dialect=session.bind.dialect) for column in visit_table.columns)}
        )  
    '''))
    session.execute(create_table_statement)
    session.execute(create_table_statement2)
    session.execute(create_table_statement3)
    session.commit()


# function for product add in that store
def product_add(session, tenant):
    add_product = Product(
        id=str(uuid.uuid4()),
        name=request.form.get("name"),
        pinfo=request.form.get("pinfo"),
        pdesc=request.form.get("pdesc"),
        price=request.form.get("price")
    )
    session.add(add_product)
    session.commit()
    return redirect(url_for('store_page.store_home', tenant=tenant))


# for add store to archive
def add_arch_store(tenant):
    if current_user.is_admin == True:
        store = New_store.query.filter_by(sname=tenant).first()
        store.is_arch = True
        db.session.commit()


# for edit  exist store's details
def update_store(store, db):
    store.sname = request.form.get('tname')
    store.semail = request.form.get('temail')
    store.sphone = request.form.get('tphone')
    store.spassword = request.form.get('tpassword')
    store.update_at = date.today()

    db.session.commit()


# for uodate on their store details
def new_update(store_name, user_email):
    new_update_details = Trace(
        id=str(uuid.uuid4()),
        update_on=store_name,
        update_by=user_email,
    )
    db.session.add(new_update_details)
    db.session.commit()


# 
def visitors(session, tenant):
    Visit.__table__.schema = tenant
    id = str(uuid.uuid4())
    visitor_id = current_user.id
    visit_at = tenant
    visit_date = date.today().strftime('%Y-%m-%d')
    existing_visit = Visit.query.filter(Visit.visitor_id == visitor_id, Visit.visit_date == visit_date,visit_at == tenant).first()

    if existing_visit:
        return 'Data already exists'

    new_visit = Visit(id=id,visitor_id=visitor_id, visit_at=visit_at, visit_date=visit_date)
    session.add(new_visit)
    session.commit()

    return existing_visit


# take a suggestion from user
def suggestion(session):
    id = str(uuid.uuid4())
    suggestion_title = request.form.get("suggestion_title")
    suggestion_desc = request.form.get("suggestion_desc")
    suggestion_by = current_user.id
    suggestion_at = date.today()
    suggest = Suggestion(id=id, suggestion_title=suggestion_title, suggestion_desc=suggestion_desc, suggestion_by=suggestion_by, suggestion_at=suggestion_at)
    session.add(suggest)
    session.commit()
    session.close()
    return suggest