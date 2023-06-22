from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from common.database import db
from common.models import Signup
from tenants.user.service import authenticate, signup_user


user_api = Blueprint('user_api',__name__,template_folder='templates',static_folder='static')


@user_api.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = signup_user()
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))   
    return render_template("form.html")

@user_api.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = authenticate(email, password)
        if user:
            login_user(user)
            return redirect(url_for('admin_page.admin_home', user_id=user.id))
        else:
            msg = 'Username or Password is wrong'
            return render_template('form.html', msg=msg)

    return render_template('form.html')

@user_api.route("/profile")
@login_required
def profile():
    user=current_user
    return render_template('profile.html',name=user.name,email=user.email,phone=user.phone)

@user_api.route('/logout')
@login_required
def logout():   
    logout_user()
    Signup.is_active=False   
    return redirect('login')