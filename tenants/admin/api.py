from datetime import date
import uuid
from flask import Blueprint, g, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from common.models import Trace, new_store
from common.database import switch_tenant,db
from tenants.admin.service import create_table_store, details_user, find_store, store_add
admin = Blueprint('admin_page', __name__, template_folder='templates', static_folder='static')
    
engine = create_engine('postgresql://postgres:postgres@localhost:1111/postgres')
Session = sessionmaker(bind=engine)
session  = Session()

@admin.route("/home", methods=['GET', 'POST'])
@login_required
def admin_home():
    user=details_user()
    if current_user.is_admin == True:
        add = session.query(new_store).filter(new_store.create_by == current_user.email).all()
    else :
        user = details_user()
        search=add = new_store.query.all()
        if request.method == 'POST':
            search = request.form.get("search").lower().replace(" ", "_")
            if search:
                search_stores, msg = find_store(search)  
                return render_template('admin/main_home.html', user=user, add=add, search_stores=search_stores, msg=msg)
            else:
                return render_template('admin/main_home.html', user=user, add=add)
    return render_template('admin/main_home.html',use=user,add=add)


@admin.route('/edit_store/<string:tenant>', methods=['GET', 'POST'])
@login_required
def edit_store(tenant):
    if current_user.is_admin == True :
        schema = tenant
        store = new_store.query.filter_by(sname=tenant).first()
        if request.method == 'POST':
            store.sname = request.form.get('tname')
            store.semail = request.form.get('temail')
            store.sphone = request.form.get('tphone')
            store.spassword = request.form.get('tpassword')

            db.session.commit()
            new_update = Trace(
                id=str(uuid.uuid4()),
                update_on=store.sname,
                update_by=current_user.email,
            )
            new_store.update_at = date.today()
            db.session.add(new_update)
            db.session.commit()
            return redirect(url_for('admin_page.admin_home'))
    else:
        return "unautorized",401

    return render_template('admin/edit_store.html', store=store, schema=schema)


@admin.route('/add_new', methods=['GET', 'POST'])
@switch_tenant
def add_new():
    if request.method == 'POST':
        new_one = store_add()

        try:
            schema = g.tenant = new_one.sname 
            db.choose_tenant(schema)
            session.add(new_one)
            create_table_store(session,schema)
            session.commit()   
            return redirect(url_for('admin_page.admin_home'))
        except Exception as e:
            return str(e)
        finally:
            session.close()
    
    return render_template('admin/add_new.html')



