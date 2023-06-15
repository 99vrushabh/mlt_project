import uuid
from flask import Blueprint, g, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from common.models import new_store

admin = Blueprint('admin_page', __name__, template_folder='templates', static_folder='static')
    
engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
Session = sessionmaker(bind=engine)
session  = Session()

@admin.route("/home",methods=['GET','POST'])
@login_required
def admin_home():
        add=session.query(new_store).filter(new_store.create_by == current_user.email).all()
        return render_template('admin/main_home.html',add=add)

@admin.route('/add_new', methods=['GET', 'POST'])
def add_new():
    if request.method == 'POST':
        id =str(uuid.uuid4())
        sname = request.form.get('sname').lower().replace(" ","_")
        semail = request.form.get('semail')
        spassword = request.form.get('spassword')
        create_by = str(current_user.email)
        new_one = new_store(id=id,sname=sname, semail=semail, spassword=spassword,create_by=create_by)
        
        try:
            schemas = sname
            breakpoint()
            session.execute(text('CREATE SCHEMA IF NOT EXISTS "{}"'.format(schemas)))
            session.execute('SET search_path TO "{}"'.format(schemas))
            session.execute(text(f'''
                CREATE TABLE IF NOT EXISTS "{schemas}"."product" (
                    "id" VARCHAR(50) PRIMARY KEY,
                    "name" VARCHAR(50) NOT NULL,
                    "pinfo" VARCHAR(150),
                    "pdesc" VARCHAR(150),
                    "price" FLOAT NOT NULL
                )
            '''))
            
            session.add(new_one)
            session.commit()    
            
            return redirect(url_for('admin_page.admin_home',schemas=schemas,_schemas=schemas)) 
        except Exception as e:
            session.rollback()
            return str(e)
        
        finally:
            session.close()
            return schemas
    return render_template('admin/add_new.html')


    

