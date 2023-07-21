import uuid
from flask import Blueprint, g, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from common.database import switch_tenant
from common.models import Visit
from tenants.store.service import all_products,  search_products
from tenants.admin.service import product_add, visitors

NoStoremsg = "Store is not Registerd..."
NoProductmsg = "Product is not found..."

store_api = Blueprint('store_page', __name__,
                  template_folder='templates', static_folder='static')
engine = create_engine('postgresql://postgres:postgres@localhost:1111/postgres')
Session = sessionmaker(bind=engine)
session = Session()
img1 = "/static/photos/one.jpg"
img2 = "/static/photos/two.jpg"
img3 = "/static/photos/three.jpg"
img4 = "/static/photos/four.jpg"
img5 = "/static/photos/five.jpg"

visitor_count = 0   


@store_api.route('/store_home/<string:tenant>')
@login_required 
def store_home(tenant):
    schema = tenant
    visit_users = visitors(session,tenant)
    return render_template('store/home.html', schema=tenant, img1=img1, img2=img2, img3=img3, img4=img4, img5=img5)


@store_api.route('/store_menu/<string:tenant>', methods=['GET', 'POST'])
def store_menu(tenant):
    schema = tenant
    search_result = None 
    try:
        with session.begin():
            result = all_products(session, schema)
            if request.method == 'POST':
                search = request.form.get('search')
                search_result = search_products(session, search, schema)
                return render_template('store/menu.html', schema=tenant, result=result,msg=NoProductmsg ,search_result=search_result)

    except SQLAlchemyError:
        return NoStoremsg
    return render_template('store/menu.html', schema=tenant, result=result ,search_result=search_result)

@store_api.route('/store_rewards/<string:tenant>')
def store_rewards(tenant):
    tenant=tenant
    return render_template('store/rewards.html',schema=tenant)

from flask import g

@store_api.route('/add_product/<string:tenant>', methods=['GET', 'POST'])
@switch_tenant
def add_product(tenant):        
    schema = g.tenant = tenant
    try:
        if request.method == 'POST':
            if schema:
                session.execute(text(f"set search_path to {tenant}"))
                add_new_product = product_add(session,tenant)
                return add_new_product
            else:   
                return NoStoremsg
    except Exception as e:
        return str(e)
    finally:
        session.close()
    return render_template('store/product.html', tenant=tenant)

@store_api.route('/order/<string:tenant>')
@switch_tenant
def order(tenant):
    g.tenant= tenant
    name = current_user.name
    return render_template('store/order.html',tenant=tenant,name=name)