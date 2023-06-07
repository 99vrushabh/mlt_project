from flask import Blueprint, current_app, redirect, render_template, request
from flask_login import login_required
import psycopg2
from common.database import db
from common.models import new_store

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
