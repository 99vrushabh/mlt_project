import uuid
from flask import Flask, flash, g, jsonify, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from common.database import *
from common.models import Signup
from tenants.admin.api import admin
from tenants.store.api import store


def create_app():
    app=Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:1111/postgres'
    app.config['SQLALCHEMY_BINDS']={
        'test1':'postgresql://postgres:postgres@localhost:2222/test1',
        'test2' :'postgresql://postgres:postgres@localhost:1234/test2'
    }
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'vrushabh@_2611'
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.register_blueprint(admin)
    app.register_blueprint(store)
    return app


app=create_app()
login_manager = LoginManager()
login_manager.init_app(app) 

@login_manager.user_loader
def load_user(user_id):
    return Signup.query.get(user_id)

# apis 
@app.before_request
def before_request():
    tenant = request.headers.get('tenant')
    if tenant:
        db.choose_tenant(tenant)
        db.create_all()

@app.route('/')
def home():
    return redirect('login')
   
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = Signup(
            id =str(uuid.uuid4()),
            name=request.form.get("name"),  
            email=request.form.get("email"),
            phone = request.form.get("phone"),
            password=request.form.get("password"),
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))   
    return render_template("signup.html")

@app.route('/login' ,methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = Signup.query.filter_by(
            name=request.form.get("name")).first_or_404()
        if user.password == request.form.get("password"):
            login_user(user)
            flash("you are successfuly logged in")
            notification = "Login Successfully...",200
            return redirect(url_for('admin_page.admin_home',user_id=user.id,notification=notification))
        else:
            msg = "Username or Password is wrong"
            return render_template('login.html', msg=msg)
    return render_template("login.html")

@app.route("/profile")
@login_required     
def profile():
    name=current_user.name
    email=current_user.email
    phone=current_user.phone
    return render_template('profile.html',name=name,email=email,phone=phone)

@app.route("/superadmin_userdetails")
@login_required
def details():
    if current_user.is_superadmin == True:
        user=Signup.query.all()
        return render_template('users.html',users=user)
    else:
        return jsonify({"message":"Unauthorized access"})

@app.route('/logout')
@login_required
def logout():   
    logout_user()
    Signup.is_active=False   
    return redirect('login')

if __name__ == '__main__':
    app.run(debug=True)
