from functools import wraps
from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from common.database import db
from common.models import Signup
from tenants.store.api import store


def create_app():
    app=Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/postgres'
    app.config['SECRET_KEY'] = 'vrushabh@_2611'
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.register_blueprint(store)
    return app
from sqlalchemy import create_engine



app=create_app()
active_user=0
login_manager = LoginManager()
login_manager.init_app(app) 

@login_manager.user_loader
def load_user(user_id):
    return Signup.query.get(int(user_id))
# apis  
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = Signup(
            name=request.form.get("name"),
            email=request.form.get("email"),
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
            global active_user
            active_user +=1
            return redirect(url_for('store_page.store_home'))
        else:
            msg = "Username or Password is wrong"
            return render_template('login.html', msg=msg)
    return render_template("login.html")



@app.route("/profile")
@login_required     
def profile():
    name=current_user.name
    email=current_user.email
    return render_template('profile.html',name=name,email=email)

@app.route("/superadmin_userdetails")
@login_required
def details():
    if current_user.is_superadmin == True:
        user=Signup.query.all()
        onuser=active_user
        return render_template('users.html',users=user,online=onuser)
    else:
        return jsonify({"message":"Unauthorized access"})

@app.route('/logout')
@login_required
def logout():   
    logout_user()   
    global active_user
    active_user -=1
    return redirect('login')

if __name__ == '__main__':
    app.run(debug=True)
