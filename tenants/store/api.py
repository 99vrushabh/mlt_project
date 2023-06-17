import uuid
from flask import Blueprint, g, redirect, render_template, request, url_for
from common.database import db
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from common.database import switch_tenant

store = Blueprint('store_page',__name__,template_folder='templates',static_folder='static')
engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
session  = Session()

@store.route('/store_home')
def store_home():
    return render_template('store/home.html')

@store.route('/store_menu')
def store_menu():
    return render_template('store/menu.html')

@store.route('/store_rewards')
def store_rewards():
    return render_template('store/rewards.html')

@store.route('/add_product', methods=['GET', 'POST'])
@switch_tenant
def add_product():
    tenant = g.tenant
    db.choose_tenant(tenant)
    try:
        if request.method == 'POST':
            id = str(uuid.uuid4())
            name = request.form.get("pname")
            pinfo = request.form.get("pinfo")
            pdesc = request.form.get("pdesc")
            price = request.form.get("pprice")
            
            query = text(f'INSERT INTO "product" ("id", "name", "pinfo", "pdesc", "price") '
                         f'VALUES (:id, :name, :pinfo, :pdesc, :price)')

            db.session.execute(query, {'id': id, 'name': name, 'pinfo': pinfo, 'pdesc': pdesc, 'price': price})
            db.session.commit()
            return redirect(url_for('store_page.store_home'))
    except Exception as e:
        return str(e)
    
    return render_template('store/product.html')

