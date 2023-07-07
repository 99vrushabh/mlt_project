import uuid
from flask import request
from sqlalchemy import text
from common.models import Product, new_store
# function for add product in perticullar schema

def find_store(search):
    msg="fetch error"
    if search:
        search_stores = new_store.query.filter(new_store.sname.like(f'%{search}%')).all()
        if not search_stores:
            msg = "Store not found"
        return search_stores,msg
    else:
        return msg
    
def search_products(session, search, schema):
    msg=""
    if search:
        searchproducts = session.execute(
            text(f'SELECT * FROM "{schema}"."Product" WHERE LOWER(name) LIKE :value'),
            {"value": f"%{search}%"}
        )
        if not searchproducts:
            return msg
        else:
            return searchproducts
    else:
        return [],msg
    
def all_products(session, schema):
    display = text(f'SELECT * FROM "{schema}"."Product" ')
    menu = session.execute(display)
    return menu.fetchall()