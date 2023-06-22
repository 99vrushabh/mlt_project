from flask import Blueprint, g, redirect, render_template, request, url_for
from flask_login import current_user
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from common.database import switch_tenant
from tenants.store.service import all_products,  search_products
from tenants.admin.service import product_add


store_api = Blueprint('store_page', __name__,
                  template_folder='templates', static_folder='static')
engine = create_engine('postgresql://postgres:postgres@localhost:1111/postgres')
Session = sessionmaker(bind=engine)
session = Session()



@store_api.route('/store_home/<string:tenant>')
def store_home(tenant):
    schema=tenant
    return render_template('store/home.html',schema=tenant)


@store_api.route('/store_menu/<string:tenant>', methods=['GET', 'POST'])
def store_menu(tenant):
    schema = tenant
    search_result = None
    try:
        with session.begin():
            result = all_products(session, schema)
            if request.method == 'POST':
                search = request.form.get('search')
                search_result, msg = search_products(session, search, schema)
                msg="Product not found"
                return render_template('store/menu.html', schema=tenant, result=result,msg=msg ,search_result=search_result)
                
    except SQLAlchemyError as e:
        return str(e)
    return render_template('store/menu.html', schema=tenant, result=result ,search_result=search_result)

@store_api.route('/store_rewards/<string:tenant>')
def store_rewards(tenant):
    tenant=tenant
    return render_template('store/rewards.html',schema=tenant)


@store_api.route('/add_product/<string:tenant>', methods=['GET', 'POST'])
@switch_tenant
def add_product(tenant):
    schema=g.tenant= tenant
    try:
        if request.method == 'POST':
            if schema:
                add_new_product = product_add()
                session.add(add_new_product)
                session.commit()
                return redirect(url_for('store_page.store_home',tenant=tenant))
            else:   
                return "Tenant not specified"
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