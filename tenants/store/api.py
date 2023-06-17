from functools import wraps
import uuid
from flask import Blueprint, g, redirect, render_template, request, url_for
from common.database import db
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from common.database import switch_tenant

store = Blueprint('store_page', __name__,
                  template_folder='templates', static_folder='static')
engine = create_engine('postgresql://postgres:postgres@localhost:1111/postgres')
Session = sessionmaker(bind=engine)
session = Session()



@store.route('/store_home/<string:tenant>')
def store_home(tenant):
    schema=tenant
    return render_template('store/home.html',schema=tenant)


@store.route('/store_menu/<string:tenant>')
def store_menu(tenant):
    schema=tenant
    display = text(f'SELECT * FROM "{schema}"."product" ')
    menu=session.execute(display)
    result = menu.fetchall()
    return render_template('store/menu.html',schema=tenant,result=result)


@store.route('/store_rewards/<string:tenant>')
def store_rewards(tenant):
    tenant=tenant
    return render_template('store/rewards.html',schema=tenant)


@store.route('/add_product/<string:tenant>', methods=['GET', 'POST'])
@switch_tenant
def add_product(tenant):
    g.tenant= tenant
    try:
        if request.method == 'POST':
            id = str(uuid.uuid4())
            name = request.form.get("pname")
            pinfo = request.form.get("pinfo")
            pdesc = request.form.get("pdesc")
            price = request.form.get("pprice")
            schema = tenant

            if schema:
                query = text(f'INSERT INTO "{schema}"."product" ("id", "name", "pinfo", "pdesc", "price") '
                             f'VALUES (:id, :name, :pinfo, :pdesc, :price)')

                db.session.execute(
                    query, {'id': id, 'name': name, 'pinfo': pinfo, 'pdesc': pdesc, 'price': price})
                db.session.commit()
                return redirect(url_for('store_page.store_home',tenant=tenant))
            else:   
                return "Tenant not specified"
    except Exception as e:
        return str(e)

    return render_template('store/product.html', tenant=tenant)

