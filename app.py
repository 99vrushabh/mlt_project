from flask import Flask, jsonify, redirect, render_template, request
from flask_login import LoginManager, current_user, login_required
from common.database import *
from common.models import Signup
from tenants.admin.api import admin_api
from tenants.store.api import store_api
from tenants.user.api import user_api
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
    app.register_blueprint(user_api)
    app.register_blueprint(admin_api)
    app.register_blueprint(store_api)
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
   

@app.route("/superadmin_userdetails")
@login_required
def details():
    if current_user.is_superadmin == True:
        user=Signup.query.all()
        return render_template('users.html',users=user)
    else:
        return jsonify({"msg":"Unauthorized access"})



if __name__ == '__main__':
    app.run(debug=True)
