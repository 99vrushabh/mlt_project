from flask import Blueprint, redirect, render_template, request
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
        new_one=new_store(sname = request.form.get('sname'),  
        semail = request.form.get('semail'),
        spassword = request.form.get('spassword') ) 
        sname=request.form.get('sname')
        conn = psycopg2.connect('postgresql://postgres:postgres@localhost:5432/postgres')
        cursor = conn.cursor()
        try:
            cursor.execute(f'CREATE SCHEMA IF NOT EXISTS {sname.lower().replace(" ","_")};')
            db.session.add(new_one)
            db.session.commit()   
            conn.commit()
            return redirect('home')
        except Exception as e:
            conn.rollback()
            return str(e)
        finally:
            cursor.close()
            conn.close()
    return render_template('store/add_new.html')

@store.route("/create_all")
def create_db():
    conn = psycopg2.connect('postgresql://postgres:postgres@localhost:5432/postgres')
    cursor=conn.cursor()
    breakpoint()
    cursor.execute('SELECT sname from .schema')
    schemas=cursor.fetchall()
    for schema in schemas:
        try:
            cursor.execute("SET search_path TO %s", (schema[0],))
            # Create the product table
            cursor.execute("CREATE TABLE IF NOT EXISTS products (id SERIAL PRIMARY KEY, name VARCHAR(255), price DECIMAL(10, 2))")
            # Create the order table
            cursor.execute("CREATE TABLE IF NOT EXISTS orders (id SERIAL PRIMARY KEY, product_id INTEGER REFERENCES products(id), quantity INTEGER)")

            db.commit()
        except Exception as e:
            # Handle any exceptions or errors
            print(f"Error creating tables in schema {schema[0]}: {str(e)}")
            db.rollback()

    cursor.close()
    db.close()