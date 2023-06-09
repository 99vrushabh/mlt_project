from flask import Blueprint, redirect, render_template, request
from flask_login import login_required
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from common.database import db
from common.models import Product, new_store

store = Blueprint('store_page', __name__, template_folder='templates', static_folder='static')


@store.route("/home")
@login_required
def store_home():
    add=new_store.query.all()
    return render_template('store/main_home.html',add=add)

engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
Session = sessionmaker(bind=engine)

@store.route('/add_new', methods=['GET', 'POST'])
def add_new():
    if request.method == 'POST':
        sname = request.form.get('sname')
        semail = request.form.get('semail')
        spassword = request.form.get('spassword')
        new_one = new_store(sname=sname, semail=semail, spassword=spassword)
        
        try:
            schemas = sname.lower().replace(" ", "_")
            session = Session()
            session.execute(text(f'CREATE SCHEMA IF NOT EXISTS {schemas}'))
            session.execute(text(f'SET search_path TO {schemas}'))
            session.execute(text('''
                CREATE TABLE IF NOT EXISTS product (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(50) NOT NULL,
                    price FLOAT NOT NULL
                )
            '''))
            
            # Add the new record to the session
            session.add(new_one)
            
            # Commit the changes to the database
            session.commit()
            
            return redirect('home')
        except Exception as e:
            session.rollback()
            return str(e)
        
        finally:
            session.close()
    
    return render_template('store/add_new.html')

@store.route('/add_field', methods=['GET', 'POST'])
def add_field():
    if request.method == 'POST':
        new_field1 = request.form.get('new_field1')
        new_field2 = request.form.get('new_field2')
        new_field3 = request.form.get('new_field3')
        sname = request.form.get('sname')
        try:
            schemas = sname.lower().replace(" ", "_")
            Session = sessionmaker(bind=db.engine)
            session = Session()
            session.execute(text(f'SET search_path TO {schemas}'))
            session.execute(text(f'ALTER TABLE {schemas}.product ADD COLUMN {new_field1} varchar(150) ;ALTER TABLE {schemas}.product ADD COLUMN {new_field2} varchar(150) ;ALTER TABLE {schemas}.product ADD COLUMN {new_field3} varchar(150) ;'))
            session.commit()
          
        except Exception as e:
            session.rollback()
            return str(e)
        finally:
            session.close()
        
    return render_template('admin/customize.html')   

@store.route('/menu')
def menu():
    return render_template('store/menu.html')