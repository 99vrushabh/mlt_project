from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from common.models import Signup, new_store
from common.database import switch_tenant, db
from common.service import change_tenant
from tenants.admin.service import add_arch_store, create_table_store, new_update, store_add, update_store
from tenants.store.service import find_store
from tenants.user.service import admin_user, details_user   


admin_api = Blueprint('admin_page', __name__,
                      template_folder='templates', static_folder='static')

engine = create_engine(
    'postgresql://postgres:postgres@localhost:1111/postgres')
Session = sessionmaker(bind=engine)
session = Session()


@admin_api.route("/home", methods=['GET', 'POST'])
@login_required
def admin_home():
    user = details_user()
    if current_user.is_admin == True:
        add = session.query(new_store).filter(
            new_store.create_by == current_user.email, new_store.is_arch == False).all()
    else:
        search = add = new_store.query.all()
        if request.method == 'POST':
            search = request.form.get("search").lower().replace(" ", "_")
            if search:
                search_stores, msg = find_store(search)
                return render_template('admin/main_home.html', user=user, add=add, search_stores=search_stores, msg=msg)
            else:
                return render_template('admin/main_home.html', user=user, add=add)
    return render_template('admin/main_home.html', use=user, add=add)


@admin_api.route('/edit_store/<string:tenant>', methods=['GET', 'POST'])
@login_required
def edit_store(tenant):
    if current_user.is_admin == True:
        schema = tenant
        store = new_store.query.filter_by(sname=tenant).first()
        if request.method == 'POST':
            update_store(store, db)
            new_update(store.sname, current_user.email)
            return redirect(url_for('admin_page.admin_home'))
    else:
        return "unautorized", 401

    return render_template('admin/edit_store.html', store=store, schema=schema)


@admin_api.route('/add_new', methods=['GET', 'POST'])
def add_new():
    if request.method == 'POST':
        tenant = new_one = store_add()
        user = Signup.query.filter_by(name=current_user.name).first()
        try:
            change_tenant(new_one)
            session.add(new_one)
            create_table_store(session, tenant)
            session.commit()
            admin_user(user)
            return redirect(url_for('admin_page.admin_home'))
        finally:
            session.close()

    return render_template('admin/add_new.html')


@admin_api.route('/archive/<string:tenant>', methods=['POST', 'GET'])
@login_required
@switch_tenant
def arch_store(tenant):
    if current_user.is_admin == True:
        if request.method == 'GET':
            schema_name = new_store
            change_tenant(schema_name)
            add_arch_store(tenant)
            return redirect(url_for('admin_page.archive_store'))
    else:
        return "page not found ",404


@admin_api.route('/archive_store', methods=['GET', 'POST'])
def archive_store():
    add = new_store.query.filter_by(
        is_arch=True, create_by=current_user.email).all()
    return render_template('admin/arch_store.html', add=add)


@admin_api.route('/back_store/<string:tenant>', methods=['GET', 'POST'])
@login_required
@switch_tenant
def back_store(tenant):
    if request.method == 'GET':
        schema_name = new_store
        change_tenant(schema_name)
        if current_user.is_admin == True:
            store = new_store.query.filter_by(sname=tenant).first()
            store.is_arch = False
            db.session.commit()
            return redirect(url_for('admin_page.admin_home'))
    return render_template('admin/arch_store.html')
