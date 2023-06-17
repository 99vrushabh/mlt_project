import uuid
from flask import Blueprint, g, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from common.models import new_store,Signup
from common.database import switch_tenant,db

admin = Blueprint('admin_page', __name__, template_folder='templates', static_folder='static')
    
engine = create_engine('postgresql://postgres:postgres@localhost:1111/postgres')
Session = sessionmaker(bind=engine)
session  = Session()

@admin.route("/home", methods=['GET', 'POST'])
@login_required
def admin_home():
    user = current_user.name
    notification = request.args.get('notification')
    if current_user.is_admin == True:
        add = session.query(new_store).filter(new_store.create_by == current_user.email).all()
    else :
        add = new_store.query.all()
    search = new_store.query.all()
    msg = " "

    if request.method == 'POST':
        search = request.form.get("search").lower().replace(" ", "_")
        if search:
            search_stores = new_store.query.filter(new_store.sname.like(f'%{search}%')).all()
            if not search_stores:
                msg = "Store not found"
            return render_template('admin/main_home.html', user=user, add=add, search_stores=search_stores, msg=msg, notification=notification)
        else:
            return render_template('admin/main_home.html', user=user, add=add, notification=notification)
    
    return render_template('admin/main_home.html', user=user, add=add, notification=notification)


@admin.route('/add_new', methods=['GET', 'POST'])
@login_required
@switch_tenant
def add_new():
    if request.method == 'POST':
        id = str(uuid.uuid4())
        sname = request.form.get('sname').lower().replace(" ", "_")
        semail = request.form.get('semail')
        sphone = request.form.get("sphone")
        spassword = request.form.get('spassword')
        create_by = str(current_user.email)
        new_one = new_store(id=id, sname=sname, semail=semail, sphone=sphone,spassword=spassword, create_by=create_by)
        try:
            schemas = g.tenant = sname 
            db.choose_tenant(schemas)
            session.execute(text(f'CREATE SCHEMA IF NOT EXISTS {schemas}'))
            session.execute(text(f'SET search_path TO {schemas}'))
            session.execute(text(f'''
                CREATE TABLE IF NOT EXISTS "{schemas}"."product" (
                    "id" VARCHAR(50) PRIMARY KEY,
                    "name" VARCHAR(50) NOT NULL,
                    "pinfo" VARCHAR(150),
                    "pdesc" VARCHAR(150),
                    "price" FLOAT NOT NULL
                )
            ''')) 
            signup_user = session.query(Signup.name).filter(Signup.name == new_store.create_by)
            if signup_user:
                current_user.is_admin=True
            else:
                current_user.is_admin=False

            session.add(new_one)
            notification = "New store added Successfully !!"
            session.commit()    
            
            return redirect(url_for('admin_page.admin_home',notification=notification))
        except Exception as e:
            return str(e)
        finally:
            session.close()
    
    return render_template('admin/add_new.html')



