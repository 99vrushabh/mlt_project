from flask import Blueprint, current_app, redirect, render_template, request
from flask_login import login_required
import psycopg2
from common.database import db
from common.models import Product, new_store

store = Blueprint('store_page', __name__, template_folder='templates', static_folder='static')


@store.route("/home")
@login_required
def store_home():
    add=new_store.query.all()
    return render_template('store/main_home.html',add=add)

@store.route('/add_new', methods=['GET', 'POST'])
def add_new():
    if request.method == 'POST':
        sname = request.form.get('sname')
        semail = request.form.get('semail')
        spassword = request.form.get('spassword')
        # add to new_store 'table'
        new_one = new_store(sname=sname, semail=semail, spassword=spassword)

        conn = psycopg2.connect('postgresql://postgres:postgres@localhost:5432/postgres')
        cursor = conn.cursor()
        
        try:
            # Create the store-specific schema
            # its convert snmae into lower case and place _ inplace of blanc
            schemas = sname.lower().replace(" ", "_")

            #this cursor execute a schema for the database
            cursor.execute(f'CREATE SCHEMA IF NOT EXISTS {schemas};')
            
            # Set the search path to the store-specific schema
            cursor.execute(f'SET search_path TO {schemas};')
            
            # Create the Product table whene schema createdd
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS product (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(50) NOT NULL,
                    field1 varchar(50),
                    field2 varchar(50),  
                    field3 varchar(50),  

                    price FLOAT NOT NULL
                );
            ''')
            
            db.session.add(new_one)
            db.session.commit()
            conn.commit()
            
            return redirect('home')
        # next steps will shows an erro with sql
        except Exception as e:
            conn.rollback()
            return str(e)
        
        # here end cursor
        finally:
            cursor.close()
            conn.close()
    
    return render_template('store/add_new.html')

@store.route('/add_field', methods=['GET','POST'])
def add_field():
    if request.method == 'POST':
        new_field1=request.form.get('new_field1')       
        new_field2=request.form.get('new_field2')
        new_field3=request.form.get('new_field3')

        conn = psycopg2.connect('postgresql://postgres:postgres@localhost:5432/postgres')
        cursor = conn.cursor() 
        try:      
            schemas = 'ccd'
            cursor.execute(f'SET search_path TO {schemas};')
            cursor.execute(f'ALTER TABLE {schemas}.product RENAME COLUMN field1 TO {new_field1}; ')
            db.session.commit()
        except :
            conn.rollback()
            return "Field add failed"
        
        # here end cursor
        finally:
            cursor.close()
            conn.close()
            return 'Field added successfully'       
       
        
    return render_template('admin/customize.html')



   